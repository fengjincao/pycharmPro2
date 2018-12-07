# -*- coding: utf-8 -*-

def category1_reg(ins, operator, rs=None, rt=None, rd=None):
    opera_str = '{opera} R{rd}, R{rs}, R{rt}'.format(
                        opera=operator,
                        rd=rd if rd is not None else int(ins.num11_15, 2),
                        rs=rs if rs is not None else int(ins.num21_25, 2),
                        rt=rt if rt is not None else int(ins.num16_20, 2))
    return Instruction.disassembly_str_template.format(ins=ins, clas=Instruction, opcode=opera_str)


def category2_imme(ins, operator, rs=None, rt=None, imme=None):
    opera_str = '{opera} R{rt}, R{rs}, #{imme}'.format(
                        opera=operator,
                        rs=rs if rs is not None else int(ins.num21_25, 2),
                        rt=rt if rt is not None else int(ins.num16_20, 2),
                        imme=imme if imme is not None else int(ins.line[20:32], 2))
    Instruction.operation.append(opera_str)
    return Instruction.disassembly_str_template.format(ins=ins, clas=Instruction, opcode=opera_str)


def execute_opcode(opcode):
    opname = opcode.split(' ', 2)[0]


def get_code_name(code):
    return code.split(' ', 1)[0]


def get_code_operator(code):
    op_list = code.split(' ', 1)
    op_name = op_list[0]
    if op_name not in ['BREAK', 'NOP']:
        operator = op_list[1]
        operator_list = [x.strip() for x in operator.split(',')]
        reg_list = []
        for reg_item in operator_list:
            if 'R' in reg_item:
                if '(' in reg_item:
                    start_index = reg_item.find('(')
                    reg_item = reg_item[start_index:].replace('(', '').replace(')', '')
                reg_list.append(int(reg_item.replace('R', '')))
        return op_name, reg_list


def get_code_name_operator(code):
    op_list = code.split(' ', 1)
    op_name = op_list[0]
    operator_list = []
    if op_name not in ['BREAK', 'NOP']:
        operator = op_list[1]
        operator_list = [x.strip() for x in operator.split(',')]
    return op_name, operator_list


class Instruction:
    isBreak = False
    breakLocation = -1
    dataNum = 0
    PC = 64
    operation = []
    disassembly = []
    disassembly_str_template = '{ins.num26_31} {ins.num21_25} {ins.num16_20} {ins.num11_15} {ins.num6_10} {ins.num0_5}\t{clas.PC}\t{opcode}'

    def __init__(self, line):
        self.line = line
        self.number = 0
        self.num0_5 = line[26:32]
        self.num6_10 = line[21:26]
        self.num11_15 = line[16:21]
        self.num16_20 = line[11:16]
        self.num21_25 = line[6:11]
        self.num26_31 = line[:6]

    @classmethod
    def addOpera(cls, obj):
        cls.operation.append(obj)

    @classmethod
    def getPC(cls):
        return cls.PC

    @classmethod
    def addPC(cls):
        cls.PC += 4

    @classmethod
    def addDisassembled(cls, line):
        cls.disassembly.append(line)

    @classmethod
    def setBreak(cls):
        cls.breakLocation = cls.PC

    @classmethod
    def changeBreak(cls):
        cls.isBreak = True

    @classmethod
    def getBreak(cls):
        return cls.isBreak

    def Assembly(self):
        if self.getBreak() is True:
            reverNum = self.line[1:32]
            if self.line[0] == '1':
                self.number = ~(int(reverNum, 2) ^ ((1 << 31) - 1))  # int('1111111111111111111111111111111', 2)
            else:
                self.number = int(self.line[1:32], 2)
            line = '{insNum}\t{clas.PC}\t{number}'.format(insNum=self.line, clas=Instruction, number=self.number)
            self.addDisassembled(line)
            Instruction.dataNum += 1
            Simulator.Datas.update({self.PC: self.number})
            Pipeline.Datas.update({self.PC: self.number})
        else:
            num26_31 = self.num26_31
            if num26_31 == '000010':
                opera_str = 'J #{imme}'.format(imme=int(self.line[6:32], 2) << 2)
                line = Instruction.disassembly_str_template.format(ins=self, clas=Instruction, opcode=opera_str)
                self.addDisassembled(line)
            elif num26_31 == '110000':
                # ADD rt <- rs + immediate category-2
                self.addDisassembled(category2_imme(self, 'ADD'))
            elif num26_31 == '110001':
                # SUB rt <- rs - immediate category-2
                self.addDisassembled(category2_imme(self, 'SUB'))
            elif num26_31 == '100001':
                # MUL rt <- rs / immediate category-2
                self.addDisassembled(category2_imme(self, 'MUL'))
            elif num26_31 == '110010':
                # AND rt <- rs AND immediate category-2
                self.addDisassembled(category2_imme(self, 'AND'))
            elif num26_31 == '110011':
                # NOR rt <- rs NOR immediate category-2
                self.addDisassembled(category2_imme(self, 'NOR'))
            elif num26_31 == '110101':
                # SLT rt <-  rs < immediate ? 1:0 immediate category-2
                self.addDisassembled(category2_imme(self, 'SLT'))
            elif self.line[0] == '0' and self.num6_10 == '00000' and self.num0_5 == '100000':
                # ADD rt <- rs + reg category-2
                self.addDisassembled(category1_reg(self, 'ADD'))
            elif self.line[0] == '0' and self.num6_10 == '00000' and self.num0_5 == '100010':
                # SUB rt <- rs - reg category-2
                self.addDisassembled(category1_reg(self, 'SUB'))
            elif self.line[0] == '0' and self.num6_10 == '00000' and self.num0_5 == '000010':
                # MUL rt <- rs / reg category-2
                self.addDisassembled(category1_reg(self, 'MUL'))
            elif self.line[0] == '0' and self.num6_10 == '00000' and self.num0_5 == '100100':
                # AND rt <- rs AND reg category-2
                self.addDisassembled(category1_reg(self, 'AND'))
            elif self.line[0] == '0' and self.num6_10 == '00000' and self.num0_5 == '100111':
                # NOR rt <- rs NOR reg category-2
                self.addDisassembled(category1_reg(self, 'NOR'))
            elif self.line[0] == '0' and self.num6_10 == '00000' and self.num0_5 == '101010':
                # SLT rt <-  rs < reg ? 1:0 immediate category-2
                self.addDisassembled(category1_reg(self, 'SLT'))

            elif num26_31 == '000000':
                if self.num0_5 == '001000':
                    opera_str = 'JR R{rs}'.format(rs=int(self.num21_25, 2))
                    line = Instruction.disassembly_str_template.format(ins=self, clas=Instruction, opcode=opera_str)
                    self.addDisassembled(line)
                    # JR jump 跳转指定寄存器 #
                elif self.num0_5 == '100000':
                    # ADD rd = rt + rt category-1
                    self.addDisassembled(category1_reg(self, 'ADD'))
                elif self.num0_5 == '100010':
                    # SUB rd = rs - rt category-1
                    self.addDisassembled(category1_reg(self, 'SUB'))
                elif self.num0_5 == '001101':
                    # Break
                    self.changeBreak()
                    self.setBreak()
                    self.addDisassembled(
                        Instruction.disassembly_str_template.format(ins=self, clas=Instruction, opcode='BREAK'))
                elif self.num0_5 == '000000':
                    if self.line == '00000000000000000000000000000000':
                        # NOP no operation
                        self.addDisassembled(
                            Instruction.disassembly_str_template.format(ins=self, clas=Instruction, opcode='NOP'))
                    elif self.num21_25 == '00000':
                        # SLL rd <- rt << sa
                        self.addDisassembled(category2_imme(
                            self, 'SLL',
                            int(self.num16_20, 2),
                            int(self.num11_15, 2),
                            int(self.num6_10, 2)))
                elif self.num0_5 == '000010':
                    # SRL rd <- rt >> sa
                    self.addDisassembled(category2_imme(
                        self, 'SRL',
                        int(self.num16_20, 2),
                        int(self.num11_15, 2),
                        int(self.num6_10, 2)))
                elif self.num0_5 == '000011':
                    # SRA rd <- rt >> sa(airthmetic)
                    self.addDisassembled(category2_imme(
                        self, 'SRA',
                        int(self.num16_20, 2),
                        int(self.num11_15, 2),
                        int(self.num6_10, 2)))

            elif num26_31 == '000100':
                # BEQ if rs=rt then branch
                self.addDisassembled(category2_imme(
                    self, 'BEQ',
                    int(self.num16_20, 2),
                    int(self.num21_25, 2),
                    int(self.line[16:32], 2) << 2))
            elif num26_31 == '000001' and self.num16_20 == '00000':
                # BLTZ if rs<0 then branch
                opera_str = 'BLTZ R{rs}, #{imme}'.format(rs=int(self.num21_25, 2),
                                                         imme=int(self.line[16:32], 2) << 2)
                line = Instruction.disassembly_str_template.format(ins=self, clas=Instruction, opcode=opera_str)
                self.addDisassembled(line)
            elif num26_31 == '000111' and self.num16_20 == '00000':
                # BGTZ if rs>0 then branch
                opera_str = 'BGTZ R{rs}, #{imme}'.format(rs=int(self.num21_25, 2),
                                                         imme=int(self.line[16:32], 2) << 2)
                line = Instruction.disassembly_str_template.format(ins=self, clas=Instruction, opcode=opera_str)
                self.addDisassembled(line)
            elif num26_31 == '101011':
                # SW memory[base+offset] <- rt
                opera_str = 'SW R{rt}, {offset}(R{base})'.format(
                    rt=int(self.num16_20, 2),
                    offset=int(self.line[16:32], 2),
                    base=int(self.num21_25, 2))
                line = Instruction.disassembly_str_template.format(ins=self, clas=Instruction, opcode=opera_str)
                self.addDisassembled(line)
            elif num26_31 == '100011':
                # LW rt <- memory[base+offset]
                opera_str = 'LW R{rt}, {offset}(R{base})'.format(
                    rt=int(self.num16_20, 2),
                    offset=int(self.line[16:32], 2),
                    base=int(self.num21_25, 2))
                line = Instruction.disassembly_str_template.format(ins=self, clas=Instruction, opcode=opera_str)
                self.addDisassembled(line)

        self.addPC()
        self.addOpera(self)

class ScoreBoard:
    reg_using = [0 for i in range(32)]
    ALU_slot_left = 2
    ALUB_slot_lef = 2

class IF:
    IF_Current_Cycle = []
    IF_Waiting_Executed = []
    IF_every = 2
    Pre_issue_max = 4
    is_stall = False

    def __init__(self, currentPC):
        self.PC = currentPC

    def fetch(self):
        if not IF.is_stall:
            pre_issue_len = len(Issue.pre_issue_buffer)
            if pre_issue_len < 4:
                if pre_issue_len > 2:
                    self.IF_every = 1
                while self.IF_every > 0:
                    fetch_code = Pipeline.line_list.get(str(self.PC), 'None')
                    if fetch_code is not None:
                        opname = fetch_code.split(' ', 2)[0]
                        if opname in ['BREAK']:
                            Pipeline.nextPC = -2
                        if not self.stall(fetch_code, opname):
                            IF.IF_Current_Cycle.append(fetch_code)
                        self.IF_every -= 1
                        Pipeline.PC += 4

    def stall(self, fetch_code, opname):
        if opname in ['J', 'JR', 'BEQ', 'BLTZ', 'BGTZ']:
            IF.is_stall = True
            IF.IF_Waiting_Executed.append(fetch_code)
            return True
        return False


class Issue:
    pre_issue_buffer = []
    pre_issue_flag = []
    Issue_max = 2
    current_fired = []
    pre_issue_max = 4

    def __init__(self):
        self.firedLen = Issue.Issue_max
        self.pre_issue_len = len(Issue.pre_issue_buffer)

    def fire(self):
        while self.firedLen > 0:
            if self.pre_issue_len > 0:
                for code in Issue.pre_issue_buffer:
                    op_name, reg_list = get_code_operator(code)
                    if op_name in ['SW', 'LW']:
                        # MEM
                        pass
                    else:
                        canFire = True
                        for reg_willing in reg_list:
                            if ScoreBoard.reg_using[reg_willing] == 1:
                                canFire = False
                        if canFire:
                            if code in ['SLL', 'SRL', 'SRA', 'MUL']:
                                # ALUB
                                if len(ALUB.pre_ALUB) < ALUB.pre_ALUB_max:
                                    ALUB.pre_ALUB.append(code)
                                    self.fire_add_scoreboard(reg_list)
                                    Issue.current_fired.append(code)
                            else:
                                # ALU
                                if len(ALU.pre_ALU) < ALU.pre_ALU_max:
                                    ALU.pre_ALU.append(code)
                                    self.fire_add_scoreboard(reg_list)
                                    Issue.current_fired.append(code)

            self.firedLen -= 1

    def WAW_hazards(self, type):
        pass

    def WAR_hazards(self):
        pass

    def structural_hazards(self):
        pass

    def fire_add_scoreboard(self, reg_list):
        for reg_item in reg_list:
            ScoreBoard.reg_using[reg_item] = 1


class MEM:
    pre_MEM = []
    post_MEM = {}
    current_MEM = []
    MEM_max = 1
    reg_write_list = []
    reg_write_list = []
    post_MEM_code = ''

    def __init__(self):
        _num = WB.WB_max
        self.opname = ''
        self.operator = []

    def execute(self):
        if len(MEM.pre_MEM) > 0:
            code = MEM.pre_MEM[0]
            MEM.current_MEM.append(code)
            self.opname, self.operator = get_code_name_operator(code)
            if self.opname == 'SW':
                rt = int(self.operator[0].strip()[1:])
                off_base = self.operator[1].strip().split('(')
                base = int(off_base[0].strip())
                offset = int(off_base[1].strip()[1:-1])
                offset = Pipeline.Regs[offset]
                Pipeline.Datas[base + offset] = Pipeline.Regs[rt]

            elif self.opname == 'LW':
                rt = int(self.operator[0].strip()[1:])
                off_base = self.operator[1].strip().split('(')
                base = int(off_base[0])
                offset = int(off_base[1].strip()[1:-1])
                offset = Pipeline.Regs[offset]
                self.reg_result_mark(rt, Pipeline.Datas[base + offset])
                self.addPostMEM(self.reg_write_list, self.reg_write_res, code)

    def addPostMEM(self, reg_list, result_list, code):
        for reg_index, result in enumerate(reg_list):
            # ALUB.post_ALU.update({reg_index: result})
            MEM.post_MEM[reg_index] = result
            MEM.post_MEM_code = code


class ALUB:
    pre_ALUB = []
    post_ALUB = {}
    pre_ALUB_max = 4
    post_ALUB_max = 1
    current_ALUB = []
    reg_write_list = []
    reg_write_res = []
    wait_2 = 2
    post_ALUB_code = ''

    def __init__(self):
        self.opname = ''
        self.operator = []

    def execute(self):
        if len(ALUB.pre_ALUB) > 0:
            if ALUB.wait_2 > 0:
                ALUB.wait_2 -= 1
            else:
                if len(ALUB.pre_ALUB) > 1:
                    ALUB.wait_2 = 1
                else:
                    ALUB.wait_2 = 2
                code = ALUB.pre_ALUB[0]
                ALUB.current_ALUB.append(code)

                self.opname, reg_list = get_code_operator(code)
                self.opname, self.operator = get_code_name_operator(code)

                if self.opname == 'SLL':
                    rd = int(self.operator[0].strip()[1:])
                    rt = int(self.operator[1].strip()[1:])
                    sa = int(self.operator[2].strip()[1:])
                    # Pipeline.Regs[rd] = Pipeline.Regs[rt] << sa
                    self.reg_result_mark(rd, Pipeline.Regs[rt] << sa)
                elif self.opname == 'SRL':
                    # 逻辑右移
                    rd = int(self.operator[0].strip()[1:])
                    rt = int(self.operator[1].strip()[1:])
                    sa = int(self.operator[2].strip()[1:])
                    reg_sa = Pipeline.Regs[sa]
                    if reg_sa > 0:
                        reg_rt = Pipeline.Regs[rt]
                        sa_si = ['0' for i in range(32)]
                        rt_bin = bin(reg_rt)[2:]
                        rt_size = len(rt_bin)
                        sa_si[-1 * (rt_size % 32):] = list(rt_bin)
                        j = 0
                        while j < reg_sa:
                            sa_si.insert(0, '0')
                            j += 1
                        res = sa_si[:-1 * reg_sa]
                        str_res = ''.join(res)
                        # Pipeline.Regs[rd] = int(str_res, 2)
                        self.reg_result_mark(rd, int(str_res, 2))
                    else:
                        # Pipeline.Regs[rd] = Pipeline.Regs[rt]
                        self.reg_result_mark(rd, Pipeline.Regs[rt])

                elif self.opname == 'SRA':
                    # 算术右移
                    rd = int(self.operator[0].strip()[1:])
                    rt = int(self.operator[1].strip()[1:])
                    sa = int(self.operator[2].strip()[1:])
                    # Pipeline.Regs[rd] = Pipeline.Regs[rt] >> sa
                    self.reg_result_mark(rd, Pipeline.Regs[rt] >> sa)
                elif self.opname == 'MUL':
                    rd = int(self.operator[0].strip()[1:])
                    rs = int(self.operator[1].strip()[1:])
                    rt = int(self.operator[2].strip()[1:])
                    if '#' in self.operator[2]:
                        # Pipeline.Regs[rd] = Pipeline.Regs[rs] * rt
                        self.reg_result_mark(rd, Pipeline.Regs[rs] * rt)
                    else:
                        # Pipeline.Regs[rd] = Pipeline.Regs[rs] * Pipeline.Regs[rt]
                        self.reg_result_mark(rd, Pipeline.Regs[rs] * Pipeline.Regs[rt])

                self.addPostALUB(self.reg_write_list, self.reg_write_res, code)

    def addPostALUB(self, reg_list, result_list, code):
        for reg_index, result in enumerate(reg_list):
            # ALUB.post_ALU.update({reg_index: result})
            ALUB.post_ALUB[reg_index] = result
            ALUB.post_ALUB_code = code

    def reg_result_mark(self, reg_index, reg_value):
        self.reg_write_list.append(reg_index)
        self.reg_write_res.append(reg_value)


class ALU:
    pre_ALU = []
    post_ALU = {}
    pre_ALU_max = 4
    post_ALU_max = 1
    current_ALU = []
    reg_write_list = []
    reg_write_res = []
    post_ALU_code = ''

    def __init__(self):
        _pre_num = ALU.pre_ALU_max
        _post_num = ALU.pre_ALU_max
        self.opname = ''
        self.operator = []

    def execute(self):
        if len(ALU.pre_ALU) > 0:
            code = ALU.pre_ALU[0]
            ALU.current_ALU.append(code)

            self.opname, reg_list = get_code_operator(code)
            self.opname, self.operator = get_code_name_operator(code)
            if self.opname == 'NOP':
                pass
            elif self.opname == 'ADD':
                rd = int(self.operator[0].strip()[1:])
                rs = int(self.operator[1].strip()[1:])
                rt = int(self.operator[2].strip()[1:])
                if '#' in self.operator[2]:
                    Pipeline.Regs[rd] = Pipeline.Regs[rs] + rt
                    self.reg_result_mark(rd, Pipeline.Regs[rd])
                else:
                    Pipeline.Regs[rd] = Pipeline.Regs[rs] + Pipeline.Regs[rt]
                    self.reg_result_mark(rd, Pipeline.Regs[rd])

            elif self.opname == 'SUB':
                rd = int(self.operator[0].strip()[1:])
                rs = int(self.operator[1].strip()[1:])
                rt = int(self.operator[2].strip()[1:])
                if '#' in self.operator[2]:
                    Pipeline.Regs[rd] = Pipeline.Regs[rs] - rt
                    self.reg_result_mark(rd, Pipeline.Regs[rd])
                else:
                    Pipeline.Regs[rd] = Pipeline.Regs[rs] - Pipeline.Regs[rt]
                    self.reg_result_mark(rd, Pipeline.Regs[rd])
            elif self.opname == 'AND':
                rd = int(self.operator[0].strip()[1:])
                rs = int(self.operator[1].strip()[1:])
                rt = int(self.operator[2].strip()[1:])
                if '#' in self.operator[2]:
                    Pipeline.Regs[rd] = Pipeline.Regs[rs] & rt
                    self.reg_result_mark(rd, Pipeline.Regs[rd])
                else:
                    Pipeline.Regs[rd] = Pipeline.Regs[rs] & Pipeline.Regs[rt]
                    self.reg_result_mark(rd, Pipeline.Regs[rd])
            elif self.opname == 'NOR':
                rd = int(self.operator[0].strip()[1:])
                rs = int(self.operator[1].strip()[1:])
                rt = int(self.operator[2].strip()[1:])
                if '#' in self.operator[2]:
                    Pipeline.Regs[rd] = ~(Pipeline.Regs[rs] | rt)
                    self.reg_result_mark(rd, Pipeline.Regs[rd])
                else:
                    Pipeline.Regs[rd] = ~(Pipeline.Regs[rs] | Pipeline.Regs[rt])
                    self.reg_result_mark(rd, Pipeline.Regs[rd])
            elif self.opname == 'SLT':
                rd = int(self.operator[0].strip()[1:])
                rs = int(self.operator[1].strip()[1:])
                rt = int(self.operator[2].strip()[1:])
                if '#' in self.operator[2]:
                    if Pipeline.Regs[rs] < rt:
                        Pipeline.Regs[rd] = 1
                        self.reg_result_mark(rd, Pipeline.Regs[rd])
                    else:
                        Pipeline.Regs[rd] = 0
                else:
                    if Pipeline.Regs[rs] < Pipeline.Regs[rt]:
                        Pipeline.Regs[rd] = 1
                        self.reg_result_mark(rd, Pipeline.Regs[rd])
                    else:
                        Pipeline.Regs[rd] = 0
                        self.reg_result_mark(rd, Pipeline.Regs[rd])

            self.addPostALU(self.reg_write_list, self.reg_write_res, code)


    def addPostALU(self, reg_list, result_list, code):
        for reg_index, result in enumerate(reg_list):
            # ALU.post_ALU.update({reg_index: result})
            ALU.post_ALU[reg_index] = result
            ALU.post_ALU_code = code

    def reg_result_mark(self, reg_index, reg_value):
        self.reg_write_list.append(reg_index)
        self.reg_write_res.append(reg_value)


class WB:
    WB_max = 3

    def __init__(self):
        _num = WB.WB_max

    def execute(self):
        if len(ALU.post_ALU) > 0:
            for reg_id, reg_value in ALU.post_ALU.items():
                Pipeline.Regs[reg_id] = reg_value
        if len(ALUB.post_ALUB) > 0:
            for reg_id, reg_value in ALUB.post_ALUB.items():
                Pipeline.Regs[reg_id] = reg_value
        if len(MEM.post_MEM) > 0:
            for reg_id, reg_value in MEM.post_MEM.items():
                Pipeline.Regs[reg_id] = reg_value


class Pipeline:
    PC = 64
    nextPC = -1
    cycle = 1
    Regs = [0 for i in range(32)]
    Datas = {}
    Recodes = []
    line_list = {}

    def __init__(self):
        # opcode = 132 NOR R0, R3, R5
        # opcode = 164 BREAK
        self.nextPC = -1

    def execute(self):
        if_obj = IF(Pipeline.PC)
        issue_obj = Issue()
        alu_obj = ALU()
        alub_obj = ALUB()
        mem_obj = MEM()
        wb_obj = WB()

        if_obj.fetch()
        issue_obj.fire()
        alu_obj.execute()
        alub_obj.execute()
        mem_obj.execute()
        wb_obj.execute()

        self.end_of_cycle()

    def end_of_cycle(self):
        if IF.is_stall is True:
            # stall 延迟一周期，周期末置0
            IF.is_stall = False
        if len(IF.IF_Current_Cycle) > 0:
            for code in IF.IF_Current_Cycle:
                Issue.pre_issue_buffer.append(code)
            IF.IF_Current_Cycle = []
        if len(Issue.current_fired) > 0:
            for index, code in enumerate(Issue.current_fired):
                Issue.pre_issue_buffer.pop(index)
            Issue.current_fired = []
        if len(ALU.current_ALU) > 0:
            ALU.pre_ALU.pop(0)
            ALU.current_ALU = []
        if len(ALUB.current_ALUB) > 0:
            ALUB.pre_ALUB.pop(0)
            ALUB.current_ALUB = []
        Pipeline.Recodes.append({
            'cycle': Pipeline.cycle, 'PC': Pipeline.PC,
            'IF': IF.IF_Waiting_Executed[:],
            'Pre_Issue': Issue.pre_issue_buffer[:],
            'Pre_ALU': ALU.pre_ALU[:],
            'Post_ALU': ALU.post_ALU.copy(),
            'Pre_ALUB': ALUB.pre_ALUB[:],
            'Post_ALUB': ALUB.post_ALUB.copy(),
            'Pre_MEM': MEM.pre_MEM[:],
            'Post_MEM': MEM.post_MEM.copy(),
            'Regs': Pipeline.Regs[:],
            'Datas': Pipeline.Datas.copy()
        })
        Pipeline.cycle += 1


class Simulator:
    PC = 64
    Cycle = 1
    Regs = [0 for i in range(32)]
    Datas = {}
    Recodes = []

    @classmethod
    def addOneRecord(cls, opcode):
        cls.Recodes.append({'cycle': cls.Cycle,'PC': cls.PC, 'opcode': opcode, 'Regs': cls.Regs[:], 'Datas': cls.Datas.copy()})

    @classmethod
    def addCycle(cls):
        cls.Cycle += 1

    @classmethod
    def addPC(cls):
        cls.PC = str(int(cls.PC) + 4)

    def __init__(self, opcode):
        # opcode = 132 NOR R0, R3, R5
        op_list = opcode.split(' ', 2)
        self.PC = op_list[0]
        self.opname = op_list[1]
        if 'BREAK' not in self.opname:
            self.operator = op_list[2].split(',')
        self.nextPC = -1
        self.opcode = opcode

    def execute(self):
        if self.opname == 'J':
            new_PC = int(self.operator[0].strip()[1:])
            self.nextPC = new_PC
        elif self.opname == 'JR':
            reg_index = int(self.operator[0].strip()[1:])
            self.nextPC = Simulator.Regs[reg_index]
        elif self.opname == 'BEQ':
            rs = int(self.operator[0].strip()[1:])
            rt = int(self.operator[1].strip()[1:])
            offset = int(self.operator[2].strip()[1:])
            if Simulator.Regs[rs] == Simulator.Regs[rt]:
                self.nextPC = int(Simulator.PC) + offset + 4
        elif self.opname == 'BLTZ':
            rs = int(self.operator[0].strip()[1:])
            offset = int(self.operator[1].strip()[1:])
            if Simulator.Regs[rs] < 0:
                self.nextPC = int(Simulator.PC) + offset + 4
        elif self.opname == 'BGTZ':
            rs = int(self.operator[0].strip()[1:])
            offset = int(self.operator[1].strip()[1:])
            if Simulator.Regs[rs] > 0:
                self.nextPC = int(Simulator.PC) + offset + 4
        elif self.opname == 'BREAK':
            self.nextPC = -2
        elif self.opname == 'SW':
            rt = int(self.operator[0].strip()[1:])
            off_base = self.operator[1].strip().split('(')
            base = int(off_base[0].strip())
            offset = int(off_base[1].strip()[1:-1])
            offset = Simulator.Regs[offset]
            Simulator.Datas[base+offset] = Simulator.Regs[rt]
        elif self.opname == 'LW':
            rt = int(self.operator[0].strip()[1:])
            off_base = self.operator[1].strip().split('(')
            base = int(off_base[0])
            offset = int(off_base[1].strip()[1:-1])
            offset = Simulator.Regs[offset]
            Simulator.Regs[rt] = Simulator.Datas[base+offset]
        elif self.opname == 'SLL':
            rd = int(self.operator[0].strip()[1:])
            rt = int(self.operator[1].strip()[1:])
            sa = int(self.operator[2].strip()[1:])
            Simulator.Regs[rd] = Simulator.Regs[rt] << sa
        elif self.opname == 'SRL':
            # 逻辑右移
            rd = int(self.operator[0].strip()[1:])
            rt = int(self.operator[1].strip()[1:])
            sa = int(self.operator[2].strip()[1:])
            reg_sa = Simulator.Regs[sa]
            if reg_sa > 0:
                reg_rt = Simulator.Regs[rt]
                sa_si = ['0' for i in range(32)]
                rt_bin = bin(reg_rt)[2:]
                rt_size = len(rt_bin)
                sa_si[-1*(rt_size % 32):] = list(rt_bin)
                j = 0
                while j < reg_sa:
                    sa_si.insert(0, '0')
                    j += 1
                res = sa_si[:-1*reg_sa]
                str_res = ''.join(res)
                Simulator.Regs[rd] = int(str_res, 2)
            else:
                Simulator.Regs[rd] = Simulator.Regs[rt]

        elif self.opname == 'SRA':
            # 算术右移
            rd = int(self.operator[0].strip()[1:])
            rt = int(self.operator[1].strip()[1:])
            sa = int(self.operator[2].strip()[1:])
            Simulator.Regs[rd] = Simulator.Regs[rt] >> sa
        elif self.opname == 'NOP':
            pass
        elif self.opname == 'ADD':
            rd = int(self.operator[0].strip()[1:])
            rs = int(self.operator[1].strip()[1:])
            rt = int(self.operator[2].strip()[1:])
            if '#' in self.operator[2]:
                Simulator.Regs[rd] = Simulator.Regs[rs] + rt
            else:
                Simulator.Regs[rd] = Simulator.Regs[rs] + Simulator.Regs[rt]
        elif self.opname == 'SUB':
            rd = int(self.operator[0].strip()[1:])
            rs = int(self.operator[1].strip()[1:])
            rt = int(self.operator[2].strip()[1:])
            if '#' in self.operator[2]:
                Simulator.Regs[rd] = Simulator.Regs[rs] - rt
            else:
                Simulator.Regs[rd] = Simulator.Regs[rs] - Simulator.Regs[rt]
        elif self.opname == 'MUL':
            rd = int(self.operator[0].strip()[1:])
            rs = int(self.operator[1].strip()[1:])
            rt = int(self.operator[2].strip()[1:])
            if '#' in self.operator[2]:
                Simulator.Regs[rd] = Simulator.Regs[rs] * rt
            else:
                Simulator.Regs[rd] = Simulator.Regs[rs] * Simulator.Regs[rt]
        elif self.opname == 'AND':
            rd = int(self.operator[0].strip()[1:])
            rs = int(self.operator[1].strip()[1:])
            rt = int(self.operator[2].strip()[1:])
            if '#' in self.operator[2]:
                Simulator.Regs[rd] = Simulator.Regs[rs] & rt
            else:
                Simulator.Regs[rd] = Simulator.Regs[rs] & Simulator.Regs[rt]
        elif self.opname == 'NOR':
            rd = int(self.operator[0].strip()[1:])
            rs = int(self.operator[1].strip()[1:])
            rt = int(self.operator[2].strip()[1:])
            if '#' in self.operator[2]:
                Simulator.Regs[rd] = ~(Simulator.Regs[rs] | rt)
            else:
                Simulator.Regs[rd] = ~(Simulator.Regs[rs] | Simulator.Regs[rt])
        elif self.opname == 'SLT':
            rd = int(self.operator[0].strip()[1:])
            rs = int(self.operator[1].strip()[1:])
            rt = int(self.operator[2].strip()[1:])
            if '#' in self.operator[2]:
                if Simulator.Regs[rs] < rt :
                    Simulator.Regs[rd] = 1
                else:
                    Simulator.Regs[rd] = 0
            else:
                if Simulator.Regs[rs] < Simulator.Regs[rt]:
                    Simulator.Regs[rd] = 1
                else:
                    Simulator.Regs[rd] = 0
        self.addOneRecord(self.opcode)
        self.addCycle()
        if self.nextPC == -1:
            self.addPC()
        else:
            Simulator.PC = str(self.nextPC)



def simulator(instrs):
    generateAssemblyCode(instrs)
    simulation()


def generateAssemblyCode(instrs):
    for line in instrs:
        ins = Instruction(line[:32])
        ins.Assembly()
    writefile('./disassembly.txt', [line+'\n' for line in Instruction.disassembly])


def simulation():
    line_list = {line.split('\t')[1]: line.split('\t')[2] for line in Instruction.disassembly}
    Pipeline.line_list = line_list
    count = 0
    while int(Pipeline.PC) != -2:
        line = Pipeline()
        line.execute()

    # print(line_list)
    resp = []
    hyphens = '--------------------\n'
    blankline = '\n'
    cycle_template = 'Cycle:{T}\t{PC}\t{opera}\t{opertor}\n'
    registers = 'Registers\n'
    allRegTemplate = 'R00:\t{R[0]}\t{R[1]}\t{R[2]}\t{R[3]}\t{R[4]}\t{R[5]}\t{R[6]}\t{R[7]}\t{R[8]}\t' \
             '{R[9]}\t{R[10]}\t{R[11]}\t{R[12]}\t{R[13]}\t{R[14]}\t{R[15]}\n' \
             'R16:\t{R[16]}\t{R[17]}\t{R[18]}\t{R[19]}\t{R[20]}\t{R[21]}\t{R[22]}\t{R[23]}\t{R[24]}\t' \
             '{R[25]}\t{R[26]}\t{R[27]}\t{R[28]}\t{R[29]}\t{R[30]}\t{R[31]}\n'
    data = 'Data\n'
    for res in Simulator.Recodes:
        resp.append(hyphens)
        if 'BREAK' not in res['opcode']:
            op_list = res['opcode'].split(' ', 2)
            resp.append(cycle_template.format(T=res['cycle'], PC=op_list[0], opera=op_list[1], opertor=op_list[2]))
        else:
            op_list = res['opcode'].split(' ', 1)
            resp.append('Cycle:{T}\t{PC}\t{bre}\n'.format(T=res['cycle'],PC=op_list[0],bre='BREAK'))
        resp.append(blankline)
        resp.append(registers)
        resp.append(allRegTemplate.format(R=res['Regs']))
        resp.append(blankline)
        resp.append(data)
        dataLineNum = len(res['Datas'])
        lineNums = ((dataLineNum+8)-1) / 8
        begin_data_pc = Instruction.breakLocation + 4
        i = 0
        while i < lineNums:
            beginNum = begin_data_pc + i*32
            datastr = str(beginNum) + ':'
            for j in range(8):
                datastr += '\t' + str(res['Datas'][j*4+beginNum])
            datastr += '\n'
            resp.append(datastr)
            i += 1
        resp.append(blankline)
    writefile('./simulation.txt', resp)


def openfile(dir):
    fo = open(dir, "r")
    # print "file name: ", fo.name
    try:
        instructions = fo.readlines()
    finally:
        fo.close()
        return instructions


def writefile(dir, lines):
    fo = open(dir, "w")
    # print "write file name: ", fo.name
    try:
        fo.writelines(lines)
    finally:
        fo.close()

import sys
if len(sys.argv) > 1:
    dir = './' + sys.argv[1]
else:
    dir = './sample.txt'
lines = openfile(dir)

simulator(lines)
print 'Simulate success!'
