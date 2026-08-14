sub init()
    m.top.functionName = "loadLive"
end sub

' Descarga get_live_streams y publica el ContentNode resultante.
sub loadLive()
    url = Xtream_ApiUrl(m.top.serverUrl, m.top.username, m.top.password, "get_live_streams")
    body = httpGet(url)
    if body = "" then return
    json = ParseJson(body)
    m.top.content = Xtream_LiveToContent(json, m.top.serverUrl, m.top.username, m.top.password)
end sub

' GET síncrono dentro del Task (no bloquea la interfaz porque corre en su hilo).
function httpGet(url as string) as string
    xfer = CreateObject("roUrlTransfer")
    xfer.setUrl(url)
    xfer.setCertificatesFile("common:/certs/ca-bundle.crt")
    xfer.initClientCertificates()
    xfer.setRequest("GET")
    resp = xfer.getToString()
    if resp = invalid then return ""
    return resp
end function
