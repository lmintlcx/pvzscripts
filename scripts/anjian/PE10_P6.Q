
DimEnv pvz
pvz = Plugin.Window.Find("MainWindow", "Plants vs. Zombies")

DimEnv scene
scene = GameScene()

paoList = Array(Array(3, 1), Array(4, 1), Array(3, 3), Array(4, 3), Array(1, 5), _
    Array(2, 5), Array(3, 5), Array(4, 5), Array(5, 5), Array(6, 5))
paoCount = UBound(paoList) + 1
paoIndex = 0


DimEnv lck
lck = 0

Sub Lock()
    While (lck = 1)
        Delay 1
    Wend
    lck = 1
End Sub

Sub Unlock()
    lck = 0
End Sub


Function GameScene()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    mainobject = Plugin.Memory.Read32Bit(pvz, pvzbase + &H768)
    GameScene = Plugin.Memory.Read32Bit(pvz, mainobject + &H554c)
End Function

Function GameUI()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    GameUI = Plugin.Memory.Read32Bit(pvz, pvzbase + &H7fc)
End Function

Function GamePaused()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    mainobject = Plugin.Memory.Read32Bit(pvz, pvzbase + &H768)
    GamePaused = Plugin.Memory.Read8Bit(pvz, mainobject + &H164)
End Function

Function MouseInGame()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    mainobject = Plugin.Memory.Read32Bit(pvz, pvzbase + &H768)
    MouseInGame = Plugin.Memory.Read8Bit(pvz, mainobject + &H59)
End Function

Function GameClock()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    mainobject = Plugin.Memory.Read32Bit(pvz, pvzbase + &H768)
    GameClock = Plugin.Memory.Read32Bit(pvz, mainobject + &H5568)
End Function

Function Countdown()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    mainobject = Plugin.Memory.Read32Bit(pvz, pvzbase + &H768)
    Countdown = Plugin.Memory.Read32Bit(pvz, mainobject + &H559c)
End Function

Function HugeWaveCountdown()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    mainobject = Plugin.Memory.Read32Bit(pvz, pvzbase + &H768)
    HugeWaveCountdown = Plugin.Memory.Read32Bit(pvz, mainobject + &H55a4)
End Function

Function DanceClock()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    DanceClock = Plugin.Memory.Read32Bit(pvz, pvzbase + &H838)
End Function


Sub Sleep(time_cs)
    clock_begin_cs = GameClock()
    While (GameClock() - clock_begin_cs < time_cs)
        Delay 1
    Wend
End Sub

Sub PreJudge(time_cs, wave)
    If wave = 10 Or wave = 20 Then
        While (Countdown() - 4 > 0)
            Delay 1
        Wend
        While (HugeWaveCountdown() - time_cs > 0)
            Delay 1
        Wend
    Else
        While (Countdown() - time_cs > 0)
            Delay 1
        Wend
    End If
End Sub


Sub SelectSeed(row, col)
    x = 50 + (col - 1) * 53
    y = 160 + (row - 1) * 70
    Call Plugin.Bkgnd.LeftClick(pvz, x, y)
    Delay 200
End Sub

Sub SelectImitaterSeed(row, col)
    SaveMousePos
    Call Plugin.Bkgnd.MoveTo(pvz, 490, 550)
    Delay 20
    Call Plugin.Bkgnd.LeftClick(pvz, 490, 550)
    RestoreMousePos
    x = 215 + (col - 1) * 51
    y = 160 + (row - 1) * 72
    Delay 300
    Call Plugin.Bkgnd.LeftClick(pvz, x, y)
    Delay 200
End Sub

Sub LetsRock()
    SaveMousePos
    Call Plugin.Bkgnd.MoveTo(pvz, 234, 567)
    Delay 200
    Call Plugin.Bkgnd.LeftDown(pvz, 234, 567)
    Delay 100
    Call Plugin.Bkgnd.LeftUp(pvz, 234, 567)
    RestoreMousePos
End Sub


Sub SafeClick()
    Call Plugin.Bkgnd.RightClick(pvz, 60, 50)
End Sub

Sub Seed(index)
    Call Plugin.Bkgnd.LeftClick(pvz, 50 + 51 * index, 42)
End Sub

Sub Grid(row, col)
    If scene = 2 Or scene = 3 Then
        Call Plugin.Bkgnd.LeftClick(pvz, 80 * col, 55 + 85 * row)
    Elseif scene = 4 Or scene = 5 Then
        If col > 5.5 Then
            Call Plugin.Bkgnd.LeftClick(pvz, 80 * col, 50 + 85 * row)
        Else
            Call Plugin.Bkgnd.LeftClick(pvz, 80 * col, 50 + 85 * row + 20 * (5.5 - col))
        End If
    Else ' 0 1 6 7 8 9
        Call Plugin.Bkgnd.LeftClick(pvz, 80 * col, 40 + 100 * row)
    End If
End Sub

Sub C(index, row, col)
    Call Lock()
    Call SafeClick()
    Call Seed(index)
    Call Grid(row, col)
    Call Unlock()
End Sub

Sub P(row, col)
    paoIndex = paoIndex Mod paoCount
    paoGrid = paoList(paoIndex)
    Call Lock()
    Call SafeClick()
    For 3
        Call Grid(paoGrid(0), paoGrid(1))
    Next
    Call Grid(row, col)
    Call Unlock()
    paoIndex = paoIndex + 1
End Sub


Sub AutoCollectThread()
    While GameUI() <> 3
        Delay 100
    Wend
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    mainobject = Plugin.Memory.Read32Bit(pvz, pvzbase + &H768)
    Do
        item_count_max = Plugin.Memory.Read32Bit(pvz, mainobject + &He8)
        item_offset = Plugin.Memory.Read32Bit(pvz, mainobject + &He4)
        For index = 0 To item_count_max - 1 Step 1
            disappeared = Plugin.Memory.Read8Bit(pvz, item_offset + &H38 + &Hd8 * index)
            collected = Plugin.Memory.Read8Bit(pvz, item_offset + &H50 + &Hd8 * index)
            item_type = Plugin.Memory.Read32Bit(pvz, item_offset + &H58 + &Hd8 * index)
            If disappeared = 0 And collected = 0 And item_type >= 1 And item_type <= 6 Then
                While (GamePaused() = 1 Or MouseInGame() = 1)
                    Delay 100
                Wend
                item_x = Plugin.Memory.ReadSingle(pvz, item_offset + &H24 + &Hd8 * index)
                item_y = Plugin.Memory.ReadSingle(pvz, item_offset + &H28 + &Hd8 * index)
                If item_x >= 0.0 And item_y >= 70.0 Then
                    Call Lock()
                    Call Plugin.Bkgnd.LeftClick(pvz, item_x + 30, item_y + 30)
                    Call SafeClick()
                    Call Unlock()
                    Delay 100
                End If
            End If
        Next
    Loop While GameUI() = 3
End Sub


Sub ChoosingSeed()
    Call SelectSeed(3, 8)
    Call SelectSeed(2, 8)
    Call SelectSeed(3, 1)
    Call SelectSeed(5, 4)
    Call SelectSeed(1, 3)
    Call SelectSeed(3, 2)
    Call SelectSeed(5, 6)
    Call SelectSeed(2, 2)
    Call SelectSeed(2, 1)
    Call SelectImitaterSeed(2, 1)
End Sub

Sub A(row, col)
    Call C(5, row, col)
End Sub

Sub N(row, col)
    Call C(3, row, col)
    Call C(2, row, col)
    Call C(4, row, col)
End Sub


Sub Waves()
    For wave = 1 To 20 Step 1

        If wave = 20 Then
            Call PreJudge(150, wave)
        Elseif wave = 10 Then
            Call PreJudge(55, wave)
        Else
            Call PreJudge(95, wave)
        End If

        If wave = 20 Then
            Call P(4, 7)
            Call Sleep(95)
            Call P(2, 9)
            Call P(5, 9)
        Elseif wave = 10 Then
            Call P(2, 9)
            Call P(5, 9)
            Call Sleep(373 - 100)
            Call A(2, 9)
        Elseif wave = 6 Or wave = 15 Then
            Call Sleep(373 - 198 - 100)
            If wave = 6 Then
                Call N(3, 9)
            Elseif wave = 15 Then
                Call N(4, 9)
            End If
            Call Sleep(100)
        Else
            Call P(2, 9)
            Call P(5, 9)
            Call Sleep(100)
            If wave = 9 Then
                paoIndex = paoIndex + 4
            End If
            If wave = 19 Then
                paoIndex = paoIndex + 2
            End If
        End If

    Next
End Sub


Sub Main()
    Delay 3000
    Call ChoosingSeed()
    Delay 500
    Call LetsRock()
    ' Delay 200
    ' Call Plugin.Bkgnd.LeftClick(pvz, 320, 400)
    Delay 4000
    BeginThread AutoCollectThread
    Call Waves()
End Sub

Call Main()

