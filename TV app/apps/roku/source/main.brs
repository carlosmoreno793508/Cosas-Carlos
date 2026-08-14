' Punto de entrada del canal Roku de MoreTV.
' Crea la escena SceneGraph principal y arranca el bucle de eventos.
sub Main()
    screen = CreateObject("roSGScreen")
    port = CreateObject("roMessagePort")
    screen.setMessagePort(port)

    scene = screen.CreateScene("MainScene")
    screen.show()

    ' Configura la fuente por defecto (edita estos valores o usa un registro
    ' persistente para que el usuario los introduzca en pantalla).
    scene.serverUrl = "http://TU-SERVIDOR:8080"
    scene.username = "carlos"
    scene.password = "cambia-esto"

    while true
        msg = wait(0, port)
        if type(msg) = "roSGScreenEvent"
            if msg.isScreenClosed() then return
        end if
    end while
end sub
