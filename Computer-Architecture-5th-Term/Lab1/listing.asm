ASSEMBLY LISTING OF GENERATED OBJECT CODE

             ; FUNCTION main (BEGIN)
                                           ; SOURCE LINE # 1
                                           ; SOURCE LINE # 2
0000 7BFF              MOV     R3,#0FFH
0002 7A00        R     MOV     R2,#HIGH _?ix1000
0004 7900        R     MOV     R1,#LOW _?ix1000
0006 C003              PUSH    AR3
0008 C002              PUSH    AR2
000A C001              PUSH    AR1
000C 7B00              MOV     R3,#00H
000E 7A00        R     MOV     R2,#HIGH A
0010 7900        R     MOV     R1,#LOW A
0012 A801              MOV     R0,AR1
0014 AC02              MOV     R4,AR2
0016 AD03              MOV     R5,AR3
0018 D001              POP     AR1
001A D002              POP     AR2
001C D003              POP     AR3
001E 7E00              MOV     R6,#00H
0020 7F14              MOV     R7,#014H
0022 120000      E     LCALL   ?C?COPY
                                           ; SOURCE LINE # 4
0025 750000      R     MOV     S,#00H
0028 750000      R     MOV     S+01H,#00H
                                           ; SOURCE LINE # 5
002B 750000      R     MOV     P,#00H
002E 750001      R     MOV     P+01H,#01H
                                           ; SOURCE LINE # 6
0031 750000      R     MOV     I,#00H
0034 750001      R     MOV     I+01H,#01H
0037         ?C0001:
0037 C3                CLR     C
0038 E500        R     MOV     A,I+01H
003A 940A              SUBB    A,#0AH
003C E500        R     MOV     A,I
003E 6480              XRL     A,#080H
0040 9480              SUBB    A,#080H
0042 504E              JNC     ?C0002
                                           ; SOURCE LINE # 7
0044 AE00        R     MOV     R6,P
0046 AF00        R     MOV     R7,P+01H
0048 AD00        R     MOV     R5,I+01H
004A ED                MOV     A,R5
004B 25E0              ADD     A,ACC
004D 2400        R     ADD     A,#LOW A
004F F8                MOV     R0,A
0050 E6                MOV     A,@R0
0051 FC                MOV     R4,A
0052 08                INC     R0
0053 E6                MOV     A,@R0
0054 FD                MOV     R5,A
0055 120000      E     LCALL   ?C?IMUL
0058 8E00        R     MOV     P,R6
005A 8F00        R     MOV     P+01H,R7
                                           ; SOURCE LINE # 8
005C AF00        R     MOV     R7,I+01H
005E EF                MOV     A,R7
005F 25E0              ADD     A,ACC
0061 2400        R     ADD     A,#LOW A

0063 F8                MOV     R0,A
0064 E6                MOV     A,@R0
0065 FE                MOV     R6,A
0066 08                INC     R0
0067 E6                MOV     A,@R0
0068 FF                MOV     R7,A
0069 C3                CLR     C
006A EE                MOV     A,R6
006B 6480              XRL     A,#080H
006D 9480              SUBB    A,#080H
006F 5017              JNC     ?C0003
                                           ; SOURCE LINE # 9
0071 AF00        R     MOV     R7,I+01H
0073 EF                MOV     A,R7
0074 25E0              ADD     A,ACC
0076 2400        R     ADD     A,#LOW A
0078 F8                MOV     R0,A
0079 E6                MOV     A,@R0
007A FE                MOV     R6,A
007B 08                INC     R0
007C E6                MOV     A,@R0
007D FF                MOV     R7,A
007E EF                MOV     A,R7
007F 2500        R     ADD     A,S+01H
0081 F500        R     MOV     S+01H,A
0083 EE                MOV     A,R6
0084 3500        R     ADDC    A,S
0086 F500        R     MOV     S,A
                                           ; SOURCE LINE # 10
                                           ; SOURCE LINE # 11
0088         ?C0003:
0088 0500        R     INC     I+01H
008A E500        R     MOV     A,I+01H
008C 7002              JNZ     ?C0006
008E 0500        R     INC     I
0090         ?C0006:
0090 80A5              SJMP    ?C0001
0092         ?C0002:
                                           ; SOURCE LINE # 12
0092 E4                CLR     A
0093 7E00              MOV     R6,#00H
0095 7F00              MOV     R7,#00H
                                           ; SOURCE LINE # 13
0097 22                RET     
             ; FUNCTION main (END)



MODULE INFORMATION:   STATIC OVERLAYABLE
   CODE SIZE        =    152    ----
   CONSTANT SIZE    =     20    ----
   XDATA SIZE       =   ----    ----
   PDATA SIZE       =   ----    ----
   DATA SIZE        =     26    ----
   IDATA SIZE       =   ----    ----
   BIT SIZE         =   ----    ----
END OF MODULE INFORMATION.


C51 COMPILATION COMPLETE.  0 WARNING(S),  0 ERROR(S)
