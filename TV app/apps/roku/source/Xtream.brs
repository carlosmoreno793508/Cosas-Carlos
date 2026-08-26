' Cliente Xtream Codes en BrightScript (equivalente a packages/core/src/xtream.ts).
' Solo construye URLs y normaliza JSON; la descarga la hace el Task de red.

' Quita la barra final de la URL base.
function Xtream_TrimSlash(url as string) as string
    while Len(url) > 0 and Right(url, 1) = "/"
        url = Left(url, Len(url) - 1)
    end while
    return url
end function

' URL de la API player_api.php para una acción dada.
function Xtream_ApiUrl(base as string, user as string, pass as string, action as string) as string
    b = Xtream_TrimSlash(base)
    return b + "/player_api.php?username=" + user + "&password=" + pass + "&action=" + action
end function

' URL de reproducción de un stream según su tipo (live/movie/series).
function Xtream_StreamUrl(base as string, user as string, pass as string, kind as string, id as string, ext as string) as string
    b = Xtream_TrimSlash(base)
    segment = "live"
    if kind = "movie" then segment = "movie"
    if kind = "series" then segment = "series"
    return b + "/" + segment + "/" + user + "/" + pass + "/" + id + "." + ext
end function

' Convierte el arreglo JSON de get_live_streams en nodos de contenido de Roku.
function Xtream_LiveToContent(json as object, base as string, user as string, pass as string) as object
    root = CreateObject("roSGNode", "ContentNode")
    if json = invalid then return root
    for each s in json
        item = root.CreateChild("ContentNode")
        item.title = s.name
        item.HDPosterUrl = s.stream_icon
        item.streamFormat = "hls"
        item.url = Xtream_StreamUrl(base, user, pass, "live", Stri(s.stream_id).Trim(), "m3u8")
    end for
    return root
end function

' Convierte get_vod_streams en nodos de contenido (películas).
function Xtream_MoviesToContent(json as object, base as string, user as string, pass as string) as object
    root = CreateObject("roSGNode", "ContentNode")
    if json = invalid then return root
    for each m in json
        ext = m.container_extension
        if ext = invalid or ext = "" then ext = "mp4"
        item = root.CreateChild("ContentNode")
        item.title = m.name
        item.HDPosterUrl = m.stream_icon
        item.url = Xtream_StreamUrl(base, user, pass, "movie", Stri(m.stream_id).Trim(), ext)
    end for
    return root
end function
