import type { Category, MediaItem } from "@tvapp/core";

/**
 * Rejilla de canales/contenido, navegable con el D-pad. Muestra las categorías
 * como filtro lateral y los items como tarjetas grandes (10-foot UI).
 */
export function ChannelGrid({
  categories,
  items,
  activeCategory,
  onSelectCategory,
  onPlay,
}: {
  categories: Category[];
  items: MediaItem[];
  activeCategory: string | null;
  onSelectCategory: (id: string | null) => void;
  onPlay: (item: MediaItem) => void;
}) {
  const filtered = activeCategory ? items.filter((i) => i.group === activeCategory) : items;

  return (
    <div className="browse">
      <aside className="browse__cats">
        <button
          data-focusable
          className={`cat ${activeCategory === null ? "is-active" : ""}`}
          onClick={() => onSelectCategory(null)}
        >
          Todos
        </button>
        {categories.map((c) => (
          <button
            key={c.id}
            data-focusable
            className={`cat ${activeCategory === c.id ? "is-active" : ""}`}
            onClick={() => onSelectCategory(c.id)}
          >
            {c.name}
          </button>
        ))}
      </aside>

      <section className="browse__grid">
        {filtered.length === 0 && <p className="empty">No hay contenido en esta categoría.</p>}
        {filtered.map((item) => (
          <button key={item.id} data-focusable className="card" onClick={() => onPlay(item)}>
            {item.logo ? (
              <img className="card__logo" src={item.logo} alt="" loading="lazy" />
            ) : (
              <div className="card__logo card__logo--placeholder">{item.title.slice(0, 2)}</div>
            )}
            <span className="card__title">{item.title}</span>
          </button>
        ))}
      </section>
    </div>
  );
}
