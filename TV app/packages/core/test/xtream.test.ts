import { test } from "node:test";
import assert from "node:assert/strict";
import { XtreamClient, fromPlaylist } from "../src/xtream.ts";
import type { FetchLike } from "../src/xtream.ts";

/** fetch falso que devuelve respuestas predefinidas por URL (subcadena). */
function fakeFetch(routes: Array<[string, unknown]>): FetchLike {
  return async (url: string) => {
    const hit = routes.find(([frag]) => url.includes(frag));
    if (!hit) {
      return { ok: false, status: 404, json: async () => ({}), text: async () => "" };
    }
    return {
      ok: true,
      status: 200,
      json: async () => hit[1],
      text: async () => JSON.stringify(hit[1]),
    };
  };
}

const config = {
  baseUrl: "https://portal.example.com:8080",
  username: "user1",
  password: "pass1",
};

test("buildStreamUrl arma la URL de reproducción correcta", () => {
  const c = new XtreamClient(config, fakeFetch([]));
  assert.equal(
    c.buildStreamUrl("live", 42, "m3u8"),
    "https://portal.example.com:8080/live/user1/pass1/42.m3u8",
  );
  assert.equal(
    c.buildStreamUrl("movie", 7, "mp4"),
    "https://portal.example.com:8080/movie/user1/pass1/7.mp4",
  );
});

test("getLiveStreams normaliza a MediaItem", async () => {
  const c = new XtreamClient(
    config,
    fakeFetch([
      [
        "get_live_streams",
        [
          {
            stream_id: 100,
            name: "CNN",
            stream_icon: "http://x/cnn.png",
            epg_channel_id: "cnn.us",
            category_id: "3",
          },
        ],
      ],
    ]),
  );
  const items = await c.getLiveStreams();
  assert.equal(items.length, 1);
  assert.equal(items[0].id, "live-100");
  assert.equal(items[0].title, "CNN");
  assert.equal(items[0].streamUrl, "https://portal.example.com:8080/live/user1/pass1/100.m3u8");
  assert.equal(items[0].epgId, "cnn.us");
});

test("getCategories mapea id/nombre", async () => {
  const c = new XtreamClient(
    config,
    fakeFetch([
      ["get_live_categories", [{ category_id: "3", category_name: "Noticias" }]],
    ]),
  );
  const cats = await c.getCategories("live");
  assert.deepEqual(cats, [{ id: "3", name: "Noticias", type: "live" }]);
});

test("lanza error en respuesta no OK", async () => {
  const c = new XtreamClient(config, fakeFetch([]));
  await assert.rejects(() => c.getLiveStreams(), /respondió 404/);
});

test("fromPlaylist exige credenciales", () => {
  assert.throws(
    () => fromPlaylist({ id: "1", kind: "xtream", url: "http://x", createdAt: 0 }),
    /Faltan credenciales/,
  );
});
