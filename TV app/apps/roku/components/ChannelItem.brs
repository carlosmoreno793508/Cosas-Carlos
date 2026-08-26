sub init()
    m.poster = m.top.findNode("poster")
    m.label = m.top.findNode("label")
    m.focusRing = m.top.findNode("focusRing")
end sub

' Se llama cuando la rejilla asigna el contenido del item.
sub onContentSet()
    node = m.top.itemContent
    if node = invalid then return
    m.label.text = node.title
    if node.HDPosterUrl <> invalid and node.HDPosterUrl <> ""
        m.poster.uri = node.HDPosterUrl
    end if
end sub

' Resalta el marco de foco según el porcentaje de foco (0..1) que da la rejilla.
sub onFocusChanged()
    m.focusRing.opacity = m.top.focusPercent
end sub
