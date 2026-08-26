' Lógica de la escena principal: carga los canales en vivo con un Task de red y
' los muestra en la rejilla; al elegir uno, reproduce en el nodo Video.
sub init()
    m.grid = m.top.findNode("grid")
    m.video = m.top.findNode("video")
    m.grid.observeField("itemSelected", "onItemSelected")
    m.grid.setFocus(true)

    ' Observa cuando lleguen las credenciales desde main.brs y carga contenido.
    m.top.observeField("password", "loadContent")
end sub

sub loadContent()
    if m.top.serverUrl = "" or m.top.serverUrl = invalid then return
    m.loader = CreateObject("roSGNode", "ContentLoader")
    m.loader.serverUrl = m.top.serverUrl
    m.loader.username = m.top.username
    m.loader.password = m.top.password
    m.loader.observeField("content", "onContentReady")
    m.loader.control = "RUN"
end sub

sub onContentReady()
    if m.loader.content <> invalid
        m.grid.content = m.loader.content
    end if
end sub

sub onItemSelected()
    idx = m.grid.itemSelected
    node = m.grid.content.getChild(idx)
    if node = invalid then return

    contentNode = CreateObject("roSGNode", "ContentNode")
    contentNode.url = node.url
    contentNode.title = node.title
    contentNode.streamFormat = "hls"

    m.video.content = contentNode
    m.video.visible = true
    m.video.control = "play"
    m.video.setFocus(true)
end sub

' Botón Atrás del control remoto: del video vuelve a la rejilla.
function onKeyEvent(key as string, press as boolean) as boolean
    if press and key = "back"
        if m.video.visible
            m.video.control = "stop"
            m.video.visible = false
            m.grid.setFocus(true)
            return true
        end if
    end if
    return false
end function
