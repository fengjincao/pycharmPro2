import math
import sys

class Instruction:
    instrucions=[]
    values=[]
    isBreak=False
    breakSituation=-1
    PC=64
    instruction_format='{0} {1} {2} {3} {4} {5}\t{tempPC}\t{instruction}'
    value_format='{line}\t{tempPC}\t{value}'

    def __init__(self,line):
        self.line=line
        self.instruction=''
        self.value=0
        self.dic=[line[0:6],line[6:11],line[11:16],line[16:21],line[21:26],line[26:32]]

    def GenerateInstruction(self,disassembly):
        if Instruction.isBreak:
            if self.line[0]=='0':
                self.value=int(self.line,2)
            else:
                self.value=int(self.line[1:32],2)-(1<<31)
            Instruction.values.append(Instruction.value_format.format(line=self.line,tempPC=Instruction.PC,value=self.value))
            disassembly.write(Instruction.value_format.format(line=self.line,tempPC=Instruction.PC,value=self.value))
            disassembly.write('\n')
        else:
            #NOP
            if self.line[0:32]=='00000000000000000000000000000000':
                self.instruction='NOP'
            #J
            elif self.line[0:6]=='000010':
                self.instruction='J\t#{}'.format(int(self.line[6:32],2)<<2)
            #JR
            elif self.line[0:6]=='000000' and self.line[11:21]=='0000000000' and self.line[26:32]=='001000':
                self.instruction='JR\tR{}'.format(int(self.line[6:11],2))
            #BEQ
            elif self.line[0:6]=='000100':
                self.instruction='BEQ\tR{0}, R{1}, #{2}'.format(int(self.line[6:11],2),int(self.line[11:16],2),int(self.line[16:32],2)<<2)
            #BLTZ
            elif self.line[0:6]=='000001' and self.line[11:16]=='00000':
                self.instruction='BLTZ\tR{0}, #{1}'.format(int(self.line[6:11],2),int(self.line[16:32],2)<<2)
            #BGTZ
            elif self.line[0:6]=='000111' and self.line[11:16]=='00000':
                self.instruction='BGTZ\tR{0}, #{1}'.format(int(self.line[6:11],2),int(self.line[16:32],2)<<2)
            #BREAK
            elif self.line[0:6]=='000000' and self.line[26:32]=='001101':
                self.instruction='BREAK'
                Instruction.breakSituation=Instruction.PC
                Instruction.isBreak=True
            #SW
            elif self.line[0:6]=='101011':
                self.instruction='SW\tR{0}, {1}(R{2})'.format(int(self.line[11:16],2),int(self.line[16:32],2),int(self.line[6:11],2))
            #LW
            elif self.line[0:6]=='100011':
                self.instruction='LW\tR{0}, {1}(R{2})'.format(int(self.line[11:16],2),int(self.line[16:32],2),int(self.line[6:11],2))
            #SLL
            elif self.line[0:11]=='00000000000' and self.line[26:32]=='000000':
                self.instruction='SLL\tR{0}, R{1}, #{2}'.format(int(self.line[16:21],2),int(self.line[11:16],2),int(self.line[21:26],2))
            #SRL
            elif self.line[0:11]=='00000000000' and self.line[26:32]=='000010':
                self.instruction='SRL\tR{0}, R{1}, #{2}'.format(int(self.line[16:21],2),int(self.line[11:16],2),int(self.line[21:26],2))
            #SRA
            elif self.line[0:11]=='00000000000' and self.line[26:32]=='000011':
                self.instruction='SRA\tR{0}, R{1}, #{2}'.format(int(self.line[16:21],2),int(self.line[11:16],2),int(self.line[21:26],2))
            #ADD1
            elif self.line[0:6]=='000000' and self.line[21:32]=='00000100000':
                self.instruction='ADD\tR{0}, R{1}, R{2}'.format(int(self.line[16:21],2),int(self.line[6:11],2),int(self.line[11:16],2))
            #SUB1
            elif self.line[0:6]=='000000' and self.line[21:32]=='00000100010':
                self.instruction='SUB\tR{0}, R{1}, R{2}'.format(int(self.line[16:21],2),int(self.line[6:11],2),int(self.line[11:16],2))
            #MUL1
            elif self.line[0:6]=='011100' and self.line[21:32]=='00000000010':
                self.instruction='MUL\tR{0}, R{1}, R{2}'.format(int(self.line[16:21],2),int(self.line[6:11],2),int(self.line[11:16],2))
            #AND1
            elif self.line[0:6]=='000000' and self.line[21:32]=='00000100100':
                self.instruction='AND\tR{0}, R{1}, R{2}'.format(int(self.line[16:21],2),int(self.line[6:11],2),int(self.line[11:16],2))
            #NOR1
            elif self.line[0:6]=='000000' and self.line[21:32]=='00000100111':
                self.instruction='NOR\tR{0}, R{1}, R{2}'.format(int(self.line[16:21],2),int(self.line[6:11],2),int(self.line[11:16],2))
            #SLT1
            elif self.line[0:6]=='000000' and self.line[21:32]=='00000101010':
                self.instruction='SLT\tR{0}, R{1}, R{2}'.format(int(self.line[16:21],2),int(self.line[6:11],2),int(self.line[11:16],2))
            #ADD2
            elif self.line[0:6] == '110000':
                self.instruction='ADD\tR{0}, R{1}, #{2}'.format(int(self.line[11:16],2),int(self.line[6:11],2),int(self.line[16:32],2))
            #SUB2
            elif self.line[0:6] == '110001':
                self.instruction='SUB\tR{0}, R{1}, #{2}'.format(int(self.line[11:16],2),int(self.line[6:11],2),int(self.line[16:32],2))
            #MUL2
            elif self.line[0:6] == '100001':
                self.instruction='MUL\tR{0}, R{1}, #{2}'.format(int(self.line[11:16],2),int(self.line[6:11],2),int(self.line[16:32],2))
            #AND2
            elif self.line[0:6] == '110010':
                self.instruction='AND\tR{0}, R{1}, #{2}'.format(int(self.line[11:16],2),int(self.line[6:11],2),int(self.line[16:32],2))
            #NOR2
            elif self.line[0:6] == '110011':
                self.instruction='NOR\tR{0}, R{1}, #{2}'.format(int(self.line[11:16],2),int(self.line[6:11],2),int(self.line[16:32],2))
            #SLT2
            elif self.line[0:6] == '110101':
                self.instruction='SLT\tR{0}, R{1}, #{2}'.format(int(self.line[11:16],2),int(self.line[6:11],2),int(self.line[16:32],2))
            else:
                pass
            Instruction.instrucions.append(Instruction.instruction_format.format(*self.dic, tempPC=Instruction.PC, instruction=self.instruction))
            disassembly.write(Instruction.instruction_format.format(*self.dic, tempPC=Instruction.PC, instruction=self.instruction))
            disassembly.write('\n')
        Instruction.PC+=4

class Simulation:
    PC=64
    cycle=1
    registers=[]
    datas={}
    operations={}
    IF_Waiting=[]
    IF_Executed=[]
    Pre_Issue=[]
    Pre_ALU=[]
    Post_ALU=[]
    Pre_ALUB=[]
    Post_ALUB=[]
    Pre_MEM=[]
    Post_MEM=[]
    process_queue=[]
    num=1
    isBreak=False

    cycle_format = '--------------------\nCycle:{0}\n\n'
    if_unit_format = 'IF Unit:\n\tWaiting Instruction: {0}\n\tExecuted Instruction: {1}\n'
    pre_issue_format = 'Pre-Issue Buffer:\n\tEntry 0:{0}\n\tEntry 1:{1}\n\tEntry 2:{2}\n\tEntry 3:{3}\n'
    pre_ALU_format = 'Pre-ALU Queue:\n\tEntry 0:{0}\n\tEntry 1:{1}\n'
    post_ALU_format = 'Post-ALU Buffer:{0}\n'
    pre_ALUB_format = 'Pre-ALUB Queue:\n\tEntry 0:{0}\n\tEntry 1:{1}\n'
    post_ALUB_format = 'Post-ALUB Buffer:{0}\n'
    pre_MEM_format = 'Pre-MEM Queue:\n\tEntry 0:{0}\n\tEntry 1:{1}\n'
    post_MEM_format = 'Post-MEM Buffer:{0}\n\n'
    registers_format = 'Registers\nR00:\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\nR08:\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\nR16:\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\nR24:\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n\n'


def openFile(filePath):
    f = open(filePath, 'r')
    input=[]
    for line in f:
        input.append(line[:32])
    f.close()
    return input

def GenerateDisssembly(input,disassemblyPath):
    disassembly=open(disassemblyPath,'w')
    for i in range(len(input)):
        instruction=Instruction(input[i][:32])
        instruction.GenerateInstruction(disassembly)
    disassembly.close()

def GenerateSimulation(simulationPath):
    simulation=open(simulationPath,'w')
    for value in Instruction.values:
        Simulation.datas[int(value.split('\t')[1])]=int(value.split('\t')[2])
    for i in range(32):
        Simulation.registers.append(0)
    for instruction in Instruction.instrucions:
        Simulation.operations[int(instruction.split('\t',2)[1])]=instruction.split('\t',2)[2]
    while not Simulation.isBreak:
        Jump()
        Add_Pre_issue()
        Add_Pre_issue()
        Judge_Ready_To_Queue()
        Execute()
        Judge_Ready_To_Buffer()
        Judge_No_Conflict()
        Minus_One()
        str1,str2=Get_Part_Two()
        Simulation_Print_Part_One(simulation)
        Simulation_Print_Part_Two(simulation,str1,str2)
        Simulation.cycle+=1
    simulation.close()

def Minus_One():
    for i in range(len(Simulation.IF_Waiting)):
        if Simulation.IF_Waiting[i][5]>0:
            Simulation.IF_Waiting[i][5]-=1
    for i in range(len(Simulation.Pre_Issue)):
        if Simulation.Pre_Issue[i][5]>0:
            Simulation.Pre_Issue[i][5]-=1
    for i in range(len(Simulation.Pre_ALU)):
        if Simulation.Pre_ALU[i][7]>0:
            Simulation.Pre_ALU[i][7]-=1
    for i in range(len(Simulation.Pre_ALUB)):
        if Simulation.Pre_ALUB[i][7]>0:
            Simulation.Pre_ALUB[i][7]-=1
    for i in range(len(Simulation.Pre_MEM)):
        if Simulation.Pre_MEM[i][7]>0:
            Simulation.Pre_MEM[i][7]-=1

def Judge_No_Conflict():
    queue=Simulation.process_queue
    for i in range(len(queue)):
        if queue[i][5]<0:
            write=queue[i][2]
            read=queue[i][3]
            sign=True
            for j in range(i):
                tempWrite=queue[j][2]
                tempRead=queue[j][3]
                for x in range(len(write)):
                    for y in range(len(tempWrite)):
                        if write[x]==tempWrite[y]:
                            sign=False
                    for y in range(len(tempRead)):
                        if write[x]==tempRead[y]:
                            sign=False
                for x in range(len(read)):
                    for y in range(len(tempWrite)):
                        if read[x]==tempWrite[y]:
                            sign=False
            if sign:
                queue[i][5]=1
    for i in range(len(queue)):
        if queue[i][5]<0 and queue[i][1]=='LW':
            write = queue[i][2]
            read = queue[i][3]
            sign = True
            for j in range(i):
                tempSign=True
                tempWrite = queue[j][2]
                tempRead = queue[j][3]
                for x in range(len(write)):
                    for y in range(len(tempWrite)):
                        if write[x] == tempWrite[y]:
                            tempSign = False
                    for y in range(len(tempRead)):
                        if write[x] == tempRead[y]:
                            tempSign = False
                for x in range(len(read)):
                    for y in range(len(tempWrite)):
                        if read[x] == tempWrite[y]:
                            tempSign = False
                if (queue[j][5]==0 or queue[j][5]==1) and queue[j][1]=='SW':
                    tempSign=True
                if not tempSign:
                    sign=False
            if sign:
                queue[i][5]=1

def Judge_Ready_To_Buffer():
    if len(Simulation.Pre_ALU)>0 and Simulation.Pre_ALU[0][7]==0:
        Simulation.Post_ALU.append(Simulation.Pre_ALU.pop(0))
    if len(Simulation.Pre_ALUB)>0 and Simulation.Pre_ALUB[0][7]==0:
        Simulation.Post_ALUB.append(Simulation.Pre_ALUB.pop(0))
    if len(Simulation.Pre_MEM)>0 and Simulation.Pre_MEM[0][7]==0:
        if Simulation.Pre_MEM[0][1]=='LW':
            Simulation.Post_MEM.append(Simulation.Pre_MEM.pop(0))
        elif Simulation.Pre_MEM[0][1]=='SW':
            ins = Simulation.Pre_MEM[0]
            Simulation.datas[Simulation.registers[int(ins[3][1].strip('R'))] + int(ins[4][0])]=Simulation.registers[int(ins[3][0].strip('R'))]
            Simulation.Pre_MEM.pop(0)
            mark = ins[6]
            n = -1
            for i in range(len(Simulation.process_queue)):
                if Simulation.process_queue[i][6] == mark:
                    n = i
            Simulation.process_queue.pop(n)

def Execute():
    if len(Simulation.Post_MEM)!=0 and Simulation.Post_MEM[0][1]=='LW':
        ins=Simulation.Post_MEM[0]
        Simulation.registers[int(ins[2][0].strip('R'))]=Simulation.datas[Simulation.registers[int(ins[3][0].strip('R'))]+int(ins[4][0])]
        Simulation.Post_MEM.pop(0)
        mark=ins[6]
        n=-1
        for i in range(len(Simulation.process_queue)):
            if Simulation.process_queue[i][6]==mark:
                n=i
        Simulation.process_queue.pop(n)
    if len(Simulation.Post_ALUB)!=0:
        ins=Simulation.Post_ALUB[0]
        if ins[1]=='SLL':
            Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] << int(ins[4][0])
        elif ins[1]=='SRL':
            if Simulation.registers[int(ins[3][0].strip('R'))] >= 0:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] >> int(ins[4][0])
            else:
                shiftLen = int(ins[4][0])
                addition = 1 << (32 - shiftLen)
                Simulation.registers[int(ins[2][0].strip('R'))] = (Simulation.registers[int(ins[3][0].strip('R'))] >> int(ins[4][0]))+addition
        elif ins[1]=='SRA':
            Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] >> int(ins[4][0])
        elif ins[1]=='MUL':
            if '#' in ins[0]:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] * int(ins[4][0])
            else:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] * Simulation.registers[int(ins[3][1].strip('R'))]
        Simulation.Post_ALUB.pop(0)
        mark = ins[6]
        n = -1
        for i in range(len(Simulation.process_queue)):
            if Simulation.process_queue[i][6] == mark:
                n = i
        Simulation.process_queue.pop(n)
    if len(Simulation.Post_ALU)!=0:
        ins=Simulation.Post_ALU[0]
        if ins[1]=='ADD':
            if '#' in ins[0]:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] + int(ins[4][0])
            else:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] + Simulation.registers[int(ins[3][1].strip('R'))]
        elif ins[1]=='SUB':
            if '#' in ins[0]:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] - int(ins[4][0])
            else:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] - Simulation.registers[int(ins[3][1].strip('R'))]
        elif ins[1]=='AND':
            if '#' in ins[0]:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] & int(ins[4][0])
            else:
                Simulation.registers[int(ins[2][0].strip('R'))] = Simulation.registers[int(ins[3][0].strip('R'))] & Simulation.registers[int(ins[3][1].strip('R'))]
        elif ins[1]=='NOR':
            if '#' in ins[0]:
                Simulation.registers[int(ins[2][0].strip('R'))] = ~(Simulation.registers[int(ins[3][0].strip('R'))] | int(ins[4][0]))
            else:
                Simulation.registers[int(ins[2][0].strip('R'))] = ~(Simulation.registers[int(ins[3][0].strip('R'))] | Simulation.registers[int(ins[3][1].strip('R'))])
        elif ins[1]=='SLT':
            if '#' in ins[0]:
                if Simulation.registers[int(ins[3][0].strip('R'))] < int(ins[4][0]):
                    Simulation.registers[int(ins[2][0].strip('R'))] = 1
                else:
                    Simulation.registers[int(ins[2][0].strip('R'))] = 0
            else:
                if Simulation.registers[int(ins[3][0].strip('R'))] < Simulation.registers[int(ins[3][1].strip('R'))]:
                    Simulation.registers[int(ins[2][0].strip('R'))] = 1
                else:
                    Simulation.registers[int(ins[2][0].strip('R'))] = 0
        Simulation.Post_ALU.pop(0)
        mark = ins[6]
        n = -1
        for i in range(len(Simulation.process_queue)):
            if Simulation.process_queue[i][6] == mark:
                n = i
        Simulation.process_queue.pop(n)

def Jump():
    if len(Simulation.IF_Executed)!=0:
        ins=Simulation.IF_Executed[0]
        if ins[1]=='J':
            Simulation.PC=int(ins[4][0])
        elif ins[1]=='JR':
            Simulation.PC=Simulation.registers[int(ins[3][0].strip('R'))]
        elif ins[1]=='NOP':
            pass
        elif ins[1]=='BEQ':
            if Simulation.registers[int(ins[3][0].strip('R'))]==Simulation.registers[int(ins[3][1].strip('R'))]:
                Simulation.PC+=int(ins[4][0])
        elif ins[1]=='BLTZ':
            if Simulation.registers[int(ins[3][0].strip('R'))]<0:
                Simulation.PC+=int(ins[4][0])
        elif ins[1]=='BGTZ':
            if Simulation.registers[int(ins[3][0].strip('R'))]>0:
                Simulation.PC+=int(ins[4][0])
        Simulation.IF_Executed.pop(0)
        mark=ins[6]
        n=-1
        for i in range(len(Simulation.process_queue)):
            if Simulation.process_queue[i][6]==mark:
                n=i
        Simulation.process_queue.pop(n)

def Judge_Ready_To_Queue():
    if len(Simulation.IF_Waiting)!=0 and Simulation.IF_Waiting[0][5]==0:
        Simulation.IF_Executed.append(Simulation.IF_Waiting.pop(0))
    getNum=0
    for i in range(len(Simulation.Pre_Issue)):
        if Simulation.Pre_Issue[i-getNum][5]==0:
            if Simulation.Pre_Issue[i-getNum][1]=='SW' or Simulation.Pre_Issue[i-getNum][1]=='LW':
                if len(Simulation.Pre_MEM)<2:
                    temp=Simulation.Pre_Issue.pop(i-getNum)
                    temp[7]=1
                    Simulation.Pre_MEM.append(temp)
                    getNum+=1
            elif Simulation.Pre_Issue[i-getNum][1]=='SLL' or Simulation.Pre_Issue[i-getNum][1]=='SRL' or Simulation.Pre_Issue[i-getNum][1]=='SRA' or Simulation.Pre_Issue[i-getNum][1]=='MUL':
                if len(Simulation.Pre_ALUB)<2:
                    temp=Simulation.Pre_Issue.pop(i-getNum)
                    temp[7]=2
                    Simulation.Pre_ALUB.append(temp)
                    getNum+=1
            else:
                if len(Simulation.Pre_ALU)<2:
                    temp=Simulation.Pre_Issue.pop(i-getNum)
                    temp[7]=1
                    Simulation.Pre_ALU.append(temp)
                    getNum+=1

def Simulation_Print_Part_One(simulation):
    tempStringOne=''
    tempStringTwo=''
    tempStringThree=''
    tempStringFour=''
    simulation.write(Simulation.cycle_format.format(Simulation.cycle))
    if len(Simulation.IF_Waiting)==1:
        tempStringOne=Simulation.IF_Waiting[0][0]
    if len(Simulation.IF_Executed)==1:
        tempStringTwo=Simulation.IF_Executed[0][0]
    simulation.write(Simulation.if_unit_format.format(tempStringOne,tempStringTwo))
    tempStringOne=''
    tempStringTwo=''
    if len(Simulation.Pre_Issue)==1:
        tempStringOne='['+Simulation.Pre_Issue[0][0]+']'
    elif len(Simulation.Pre_Issue)==2:
        tempStringOne='['+Simulation.Pre_Issue[0][0]+']'
        tempStringTwo='['+Simulation.Pre_Issue[1][0]+']'
    elif len(Simulation.Pre_Issue)==3:
        tempStringOne='['+Simulation.Pre_Issue[0][0]+']'
        tempStringTwo='['+Simulation.Pre_Issue[1][0]+']'
        tempStringThree='['+Simulation.Pre_Issue[2][0]+']'
    elif len(Simulation.Pre_Issue)==4:
        tempStringOne='['+Simulation.Pre_Issue[0][0]+']'
        tempStringTwo='['+Simulation.Pre_Issue[1][0]+']'
        tempStringThree='['+Simulation.Pre_Issue[2][0]+']'
        tempStringFour='['+Simulation.Pre_Issue[3][0]+']'
    simulation.write(Simulation.pre_issue_format.format(tempStringOne,tempStringTwo,tempStringThree,tempStringFour))
    tempStringOne=''
    tempStringTwo=''
    if len(Simulation.Pre_ALU)==1:
        tempStringOne='['+Simulation.Pre_ALU[0][0]+']'
    elif len(Simulation.Pre_ALU)==2:
        tempStringOne='['+Simulation.Pre_ALU[0][0]+']'
        tempStringTwo='['+Simulation.Pre_ALU[1][0]+']'
    simulation.write(Simulation.pre_ALU_format.format(tempStringOne,tempStringTwo))
    tempStringOne=''
    tempStringTwo=''
    if len(Simulation.Post_ALU)==1:
        tempStringOne='['+Simulation.Post_ALU[0][0]+']'
    simulation.write(Simulation.post_ALU_format.format(tempStringOne))
    tempStringOne=''
    if len(Simulation.Pre_ALUB)==1:
        tempStringOne='['+Simulation.Pre_ALUB[0][0]+']'
    elif len(Simulation.Pre_ALUB)==2:
        tempStringOne='['+Simulation.Pre_ALUB[0][0]+']'
        tempStringTwo='['+Simulation.Pre_ALUB[1][0]+']'
    simulation.write(Simulation.pre_ALUB_format.format(tempStringOne,tempStringTwo))
    tempStringOne=''
    tempStringTwo=''
    if len(Simulation.Post_ALUB)==1:
        tempStringOne='['+Simulation.Post_ALUB[0][0]+']'
    simulation.write(Simulation.post_ALUB_format.format(tempStringOne))
    tempStringOne=''
    if len(Simulation.Pre_MEM)==1:
        tempStringOne='['+Simulation.Pre_MEM[0][0]+']'
    elif len(Simulation.Pre_MEM)==2:
        tempStringOne='['+Simulation.Pre_MEM[0][0]+']'
        tempStringTwo='['+Simulation.Pre_MEM[1][0]+']'
    simulation.write(Simulation.pre_MEM_format.format(tempStringOne,tempStringTwo))
    tempStringOne=''
    if len(Simulation.Post_MEM)==1:
        tempStringOne='['+Simulation.Post_MEM[0][0]+']'
    simulation.write(Simulation.post_MEM_format.format(tempStringOne))

def Get_Part_Two():
    str1=Simulation.registers_format.format(*Simulation.registers)
    dataNum = len(Simulation.datas.keys())
    lineNum = math.ceil(dataNum / 8)
    tempPC = Instruction.breakSituation + 4
    str2='Data\n'
    for i in range(lineNum):
        str2=str2+str(tempPC) + ':'
        if (i < lineNum - 1):
            for i in range(8):
                str2=str2+'\t' + str(Simulation.datas[tempPC])
                tempPC += 4
        else:
            for i in range(dataNum - lineNum * 8 + 8):
                str2=str2+'\t' + str(Simulation.datas[tempPC])
                tempPC += 4
        str2=str2+'\n'
    return str1,str2

def Simulation_Print_Part_Two(simulation,str1,str2):
    simulation.write(str1)
    simulation.write(str2)

def Add_Pre_issue():
    if (len(Simulation.IF_Waiting)==0 and len(Simulation.IF_Executed)==0 and len(Simulation.Pre_Issue)<4):
        tempList = []
        tempList.append(Simulation.operations[Simulation.PC])
        tempOperator = Simulation.operations[Simulation.PC].split('\t')[0]
        tempList.append(tempOperator)
        tempWriteOperands = []
        tempReadOperands = []
        tempImmediate=[]
        if Simulation.operations[Simulation.PC].split('\t')[0]=='BREAK':
            tempList.append(tempWriteOperands)
            tempList.append(tempReadOperands)
            tempList.append(tempImmediate)
            tempList.append(1)
            tempList.append(Simulation.num)
            tempList.append(1)
            Simulation.isBreak=True
            Simulation.IF_Executed.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='NOP':
            tempList.append(tempWriteOperands)
            tempList.append(tempReadOperands)
            tempList.append(tempImmediate)
            tempList.append(1)
            tempList.append(Simulation.num)
            tempList.append(1)
            Simulation.IF_Executed.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='J':
            tempList.append(tempWriteOperands)
            tempList.append(tempReadOperands)
            tempImmediate.append(Simulation.operations[Simulation.PC].split('\t')[1].strip('#'))
            tempList.append(tempImmediate)
            tempList.append(1)
            tempList.append(Simulation.num)
            tempList.append(1)
            Simulation.IF_Executed.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='JR':
            tempList.append(tempWriteOperands)
            tempReadOperands.append(Simulation.operations[Simulation.PC].split('\t')[1])
            tempList.append(tempReadOperands)
            tempList.append(tempImmediate)
            tempList.append(-1)
            tempList.append(Simulation.num)
            tempList.append(1)
            Simulation.IF_Waiting.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='BLTZ' or Simulation.operations[Simulation.PC].split('\t')[0]=='BGTZ':
            tempList.append(tempWriteOperands)
            tempString = Simulation.operations[Simulation.PC].split('\t')[1]
            tempReadOperands.append(tempString.split(' ')[0].strip(','))
            tempList.append(tempReadOperands)
            tempImmediate.append(tempString.split(' ')[1].strip('#'))
            tempList.append((tempImmediate))
            tempList.append(-1)
            tempList.append(Simulation.num)
            tempList.append(1)
            Simulation.IF_Waiting.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='BEQ':
            tempList.append(tempWriteOperands)
            tempString = Simulation.operations[Simulation.PC].split('\t')[1]
            tempReadOperands.append(tempString.split(' ')[0].strip(','))
            tempReadOperands.append(tempString.split(' ')[1].strip(','))
            tempList.append(tempReadOperands)
            tempImmediate.append(tempString.split(' ')[2].strip('#'))
            tempList.append(tempImmediate)
            tempList.append(-1)
            tempList.append(Simulation.num)
            tempList.append(1)
            Simulation.IF_Waiting.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='SW':
            tempList.append(tempWriteOperands)
            tempString = Simulation.operations[Simulation.PC].split('\t')[1]
            tempReadOperands.append(tempString.split(' ')[0].strip(','))
            tempReadOperands.append(tempString.split(' ')[1].split('(')[1].strip(')'))
            tempList.append(tempReadOperands)
            tempImmediate.append(tempString.split(' ')[1].split('(')[0])
            tempList.append(tempImmediate)
            tempList.append(-1)
            tempList.append(Simulation.num)
            tempList.append(-1)
            Simulation.Pre_Issue.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='LW':
            tempString = Simulation.operations[Simulation.PC].split('\t')[1]
            tempWriteOperands.append(tempString.split(' ')[0].strip(','))
            tempList.append(tempWriteOperands)
            tempReadOperands.append(tempString.split(' ')[1].split('(')[1].strip(')'))
            tempList.append(tempReadOperands)
            tempImmediate.append(tempString.split(' ')[1].split('(')[0])
            tempList.append(tempImmediate)
            tempList.append(-1)
            tempList.append(Simulation.num)
            tempList.append(-1)
            Simulation.Pre_Issue.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='SLL' or Simulation.operations[Simulation.PC].split('\t')[0]=='SRL' or Simulation.operations[Simulation.PC].split('\t')[0]=='SRA':
            tempString = Simulation.operations[Simulation.PC].split('\t')[1]
            tempWriteOperands.append(tempString.split(' ')[0].strip(','))
            tempList.append(tempWriteOperands)
            tempReadOperands.append(tempString.split(' ')[1].strip(','))
            tempList.append(tempReadOperands)
            tempImmediate.append(tempString.split(' ')[2].strip('#'))
            tempList.append(tempImmediate)
            tempList.append(-1)
            tempList.append(Simulation.num)
            tempList.append(-1)
            Simulation.Pre_Issue.append(tempList)
        elif Simulation.operations[Simulation.PC].split('\t')[0]=='ADD' or Simulation.operations[Simulation.PC].split('\t')[0]=='SUB' or Simulation.operations[Simulation.PC].split('\t')[0]=='AND' or Simulation.operations[Simulation.PC].split('\t')[0]=='NOR' or Simulation.operations[Simulation.PC].split('\t')[0]=='SLT' or Simulation.operations[Simulation.PC].split('\t')[0]=='MUL':
            tempString = Simulation.operations[Simulation.PC].split('\t')[1]
            tempWriteOperands.append(tempString.split(' ')[0].strip(','))
            tempList.append(tempWriteOperands)
            tempReadOperands.append(tempString.split(' ')[1].strip(','))
            if 'R' in tempString.split(' ')[2]:
                tempReadOperands.append(tempString.split(' ')[2])
                tempList.append(tempReadOperands)
                tempList.append(tempImmediate)
                tempList.append(-1)
                tempList.append(Simulation.num)
                tempList.append(-1)
                Simulation.Pre_Issue.append(tempList)
            else:
                tempList.append(tempReadOperands)
                tempImmediate.append(tempString.split(' ')[2].strip('#'))
                tempList.append(tempImmediate)
                tempList.append(-1)
                tempList.append(Simulation.num)
                tempList.append(-1)
                Simulation.Pre_Issue.append(tempList)
        Simulation.process_queue.append((tempList))
        Simulation.num+=1
        Simulation.PC+=4

if __name__=='__main__':
    # samplePath=sys.argv[1]
    # disassemblyPath=sys.argv[2]
    # simulationPath=sys.argv[3]
    samplePath ="C:\\Users\\lab-301\\Desktop\\计算机体系结构\\实验\\proj2\\sample test.txt"
    disassemblyPath ="C:\\Users\\lab-301\\Desktop\\计算机体系结构\\实验\\proj2\\disassembly test.txt"
    simulationPath ="C:\\Users\\lab-301\\Desktop\\计算机体系结构\\实验\\proj2\\simulation test.txt"
    input=openFile(samplePath)
    GenerateDisssembly(input,disassemblyPath)
    GenerateSimulation(simulationPath)