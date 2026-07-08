' Parser M3U en BrightScript (equivalente a packages/core/src/m3u.ts).
' Devuelve un ContentNode con los canales de una lista M3U extendida.
function ParseM3U(text as string, root as object) as object
    if root = invalid then root = CreateObject("roSGNode", "ContentNode")
    lines = text.Split(Chr(10))
    pendingTitle = ""
    pendingLogo = ""
    pendingGroup = "General"

    for each raw in lines
        line = raw.Trim()
        if line = "" or line = "#EXTM3U"
            ' saltar
        else if Left(line, 7) = "#EXTINF"
            pendingLogo = M3U_Attr(line, "tvg-logo")
            pendingGroup = M3U_Attr(line, "group-title")
            if pendingGroup = "" then pendingGroup = "General"
            commaIdx = M3U_LastIndexOf(line, ",")
            if commaIdx >= 0
                pendingTitle = Mid(line, commaIdx + 2).Trim()
            else
                pendingTitle = "Sin título"
            end if
        else if Left(line, 1) <> "#"
            item = root.CreateChild("ContentNode")
            item.title = pendingTitle
            item.HDPosterUrl = pendingLogo
            item.streamFormat = "hls"
            item.url = line
            pendingTitle = ""
            pendingLogo = ""
        end if
    end for
    return root
end function

' Extrae un atributo clave="valor" de una línea #EXTINF.
function M3U_Attr(line as string, key as string) as string
    needle = key + "="""
    startIdx = Instr(1, line, needle)
    if startIdx = 0 then return ""
    startIdx = startIdx + Len(needle)
    endIdx = Instr(startIdx, line, """")
    if endIdx = 0 then return ""
    return Mid(line, startIdx, endIdx - startIdx)
end function

' Índice de la última aparición de un carácter (1-based; -1 si no está).
function M3U_LastIndexOf(s as string, ch as string) as integer
    result = -1
    pos = Instr(1, s, ch)
    while pos > 0
        result = pos
        pos = Instr(pos + 1, s, ch)
    end while
    return result
end function
