/**
 * Fuentes M3U gratuitas y legales que el usuario puede añadir con un toque.
 *
 * Son listas públicas de canales de libre acceso / TV abierta y canales FAST
 * (gratuitos con anuncios). Se sirven desde iptv-org, un proyecto abierto que
 * agrega SOLO streams públicamente disponibles. El contenido lo mantiene y
 * actualiza esa fuente; MoreTV solo lo reproduce.
 *
 * Nota: la disponibilidad de cada canal depende de su emisora; iptv-org retira
 * los que dejan de ser públicos. Úsalas para TV abierta / contenido libre.
 */
export interface FreeSource {
  id: string;
  name: string;
  description: string;
  url: string;
}

export const FREE_SOURCES: FreeSource[] = [
  {
    id: "mx",
    name: "México — TV abierta",
    description: "Canales públicos de México (iptv-org)",
    url: "https://iptv-org.github.io/iptv/countries/mx.m3u",
  },
  {
    id: "mx-news",
    name: "México — Noticias",
    description: "Canales de noticias de acceso libre",
    url: "https://iptv-org.github.io/iptv/categories/news.m3u",
  },
  {
    id: "es",
    name: "España — TV abierta",
    description: "Canales públicos de España (iptv-org)",
    url: "https://iptv-org.github.io/iptv/countries/es.m3u",
  },
  {
    id: "sports",
    name: "Deportes (libre acceso)",
    description: "Canales deportivos públicos",
    url: "https://iptv-org.github.io/iptv/categories/sports.m3u",
  },
  {
    id: "movies",
    name: "Películas (FAST)",
    description: "Canales de cine gratuitos con anuncios",
    url: "https://iptv-org.github.io/iptv/categories/movies.m3u",
  },
  {
    id: "kids",
    name: "Infantil",
    description: "Canales infantiles de acceso libre",
    url: "https://iptv-org.github.io/iptv/categories/kids.m3u",
  },
];
