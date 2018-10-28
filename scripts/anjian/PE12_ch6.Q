
' Author: lmintlcx
' Date: 2018-09-05
' Description: PE超前置十二炮 ch6
' Video:
' - https://www.bilibili.com/video/av13518545/
' - https://www.youtube.com/watch?v=Xacqrr94Vik

DimEnv pvz
pvz = Plugin.Window.Find("MainWindow", "Plants vs. Zombies")

DimEnv scene
scene = GameScene()

paoList = Array(Array(1, 7), Array(2, 7), Array(3, 7), Array(4, 7), Array(5, 7), Array(6, 7), _
    Array(1, 5), Array(2, 5), Array(3, 5), Array(4, 5), Array(5, 5), Array(6, 5))
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

Function WaveCountdown()
    pvzbase = Plugin.Memory.Read32Bit(pvz, &H6a9ec0)
    mainobject = Plugin.Memory.Read32Bit(pvz, pvzbase + &H768)
    WaveCountdown = Plugin.Memory.Read32Bit(pvz, mainobject + &H559c)
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
        While (WaveCountdown() - 4 > 0)
            Delay 1
        Wend
        While (HugeWaveCountdown() - time_cs > 0)
            Delay 1
        Wend
    Else
        While (WaveCountdown() - time_cs > 0)
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
            While (GamePaused() = 1 Or MouseInGame() = 1)
                Delay 100
            Wend
            disappeared = Plugin.Memory.Read8Bit(pvz, item_offset + &H38 + &Hd8 * index)
            collected = Plugin.Memory.Read8Bit(pvz, item_offset + &H50 + &Hd8 * index)
            item_type = Plugin.Memory.Read32Bit(pvz, item_offset + &H58 + &Hd8 * index)
            If disappeared = 0 And collected = 0 And item_type >= 1 And item_type <= 6 Then
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

Sub FillIceThread()
    While GameUI() <> 3
        Delay 100
    Wend
    For count = 1 To 5 Step 1
        Call Lock()
        Call Seed(2)
        Call Grid(4, 3)
        Call Grid(3, 3)
        Call Grid(2, 1)
        Call Grid(1, 1)
        Call Seed(1)
        Call Grid(4, 3)
        Call Grid(3, 3)
        Call Grid(2, 1)
        Call Grid(1, 1)
        Call Unlock()
        If count <> 5
            Call Sleep(5010)
        End If
    Next
End Sub


Sub I()
    Call Lock()
    Call Seed(3)
    Call Grid(1, 1)
    Call Grid(2, 1)
    Call Grid(3, 3)
    Call Grid(4, 3)
    Call Unlock()
End Sub

Sub ChoosingSeed()
    Call SelectSeed(2, 7)
    Call SelectImitaterSeed(2, 7)
    Call SelectSeed(5, 4)
    Call SelectSeed(1, 3)
    Call SelectSeed(3, 2)
    Call SelectSeed(1, 4)
    Call SelectSeed(5, 2)
    Call SelectSeed(2, 6)
    Call SelectSeed(2, 2)
    Call SelectSeed(2, 1)
End Sub

Sub A(row, col)
    Call C(4, row, col)
End Sub

Sub F()
    Call C(7, 1, 9)
    Call C(8, 2, 9)
    Call C(9, 5, 9)
    Call C(10, 6, 9)
End Sub

Sub SF()
    Call C(12, 1, 9)
    Call C(12, 2, 9)
    Call C(12, 5, 9)
    Call C(12, 6, 9)
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

        If wave = 1 Or wave = 3 Or wave = 5 Or wave = 7 Or wave = 9 Or wave = 10 Or wave = 12 Or wave = 14 Or wave = 16 Or wave = 18 Then
            Call P(2, 9)
            Call P(5, 9)
            If wave = 10 Then
                Call Sleep(373 - 100)
                Call A(2, 9)
                Call Sleep(600 + 55 - (373 - 100) - 298 + 30) ' > 0
            Else
                Call Sleep(600 + 95 - 0 - 298 + 30)
            End If
            Call I()
            If wave = 9 Then
                Call Sleep(298 - 30 - 95)
                Call P(2, 8.5)
                Call P(5, 8.5)
                Call Sleep(82)
                Call F()
                Call Sleep(100)
                Call SF()
                Call Sleep(1200 + 95 - (100 + 82) - 373 - 200)
                Call P(2, 9)
                Call P(5, 9)
                Call Sleep(373 + 200 - 95)
                Call P(2, 9)
                Call P(5, 9)
            End If
        Elseif wave = 2 Or wave = 4 Or wave = 6 Or wave = 8 Or wave = 11 Or wave = 13 Or wave = 15 Or wave = 17 Or wave = 19 Then
            Call P(2, 8.5)
            Call P(5, 8.5)
            Call Sleep(82)
            Call F()
            Call Sleep(100)
            Call SF()
            Call Sleep(1200 + 95 - (100 + 82) - 373 - 200)
            Call P(2, 9)
            Call P(5, 9)
            If wave = 19 Then
                Call Sleep(373 + 200 - 95)
                Call P(2, 9)
                Call P(5, 9)
                Call Sleep(600 + 95 - 0 - 298 + 30)
                Call I()
                Call Sleep(298 - 30 - 95)
                Call P(2, 8.5)
                Call P(5, 8.5)
                paoIndex = paoIndex + 3
            End If
        Elseif wave = 20 Then
            Call P(4, 7)
            Call Sleep(95)
            Call P(2, 9)
            Call P(5, 9)
            Call Sleep(30)
            Call P(2, 9)
            Call P(5, 9)
            Call Sleep(30)
            Call P(2, 9)
            Call P(5, 9)
            Call Sleep(30)
            Call P(2, 9)
            Call P(5, 9)
        End If

        Call Sleep(100)

    Next
End Sub



Sub Main()
    Delay 3000
    Call ChoosingSeed()
    Delay 500
    Call LetsRock()
    Delay 200
    Call Plugin.Bkgnd.LeftClick(pvz, 320, 400)
    Delay 4000
    BeginThread AutoCollectThread
    BeginThread FillIceThread
    Call Waves()
End Sub

Call Main()
