import sys
import copy
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

THEMES = {
    'dark': {
        'bg': '#1a1a2e', 'panel': '#16213e', 'border': '#0f3460',
        'text': '#e0e0e0', 'sub': '#888', 'accent': '#e94560',
        'btn': '#0f3460', 'btn_hover': '#e94560',
        'board_dark': '#1b5e20', 'board_light': '#2e7d32',
        'board_border': '#4caf50', 'grid': '#388e3c',
        'chess_dark': '#4e342e', 'chess_light': '#bcaaa4',
        'chess_border': '#6d4c41', 'highlight': '#ffeb3b',
        'valid': '#76ff03', 'selected': '#ff9100',
    },
    'light': {
        'bg': '#f5f5f5', 'panel': '#ffffff', 'border': '#bdbdbd',
        'text': '#212121', 'sub': '#757575', 'accent': '#d32f2f',
        'btn': '#e0e0e0', 'btn_hover': '#d32f2f',
        'board_dark': '#388e3c', 'board_light': '#81c784',
        'board_border': '#2e7d32', 'grid': '#4caf50',
        'chess_dark': '#795548', 'chess_light': '#efebe9',
        'chess_border': '#4e342e', 'highlight': '#fbc02d',
        'valid': '#33691e', 'selected': '#e65100',
    }
}

TR = {
    'en': {
        'title': 'Board Games', 'chess': 'Chess', 'othello': 'Othello',
        'new_game': 'New Game', 'quit': 'Quit', 'theme': 'Theme',
        'lang': 'Language', 'dark': 'Dark', 'light': 'Light',
        'white': 'White', 'black': 'Black', 'turn': 'Turn',
        'score': 'Score', 'pass_turn': 'Pass', 'game_over': 'Game Over',
        'wins': 'Wins!', 'draw': 'Draw!', 'check': 'Check!',
        'checkmate': 'Checkmate!', 'stalemate': 'Stalemate!',
        'promotion': 'Promote Pawn', 'select_promo': 'Select piece:',
        'captured': 'Captured', 'undo': 'Undo', 'hint': 'Hint',
        'vs_ai': 'vs AI', 'vs_human': 'vs Human', 'mode': 'Mode',
        'ai_thinking': 'AI thinking...', 'no_moves': 'No valid moves',
        'queen': 'Queen', 'rook': 'Rook', 'bishop': 'Bishop', 'knight': 'Knight',
    },
    'zh': {
        'title': '棋盘游戏', 'chess': '国际象棋', 'othello': '黑白棋',
        'new_game': '新游戏', 'quit': '退出', 'theme': '主题',
        'lang': '语言', 'dark': '深色', 'light': '浅色',
        'white': '白方', 'black': '黑方', 'turn': '回合',
        'score': '分数', 'pass_turn': '跳过', 'game_over': '游戏结束',
        'wins': '获胜！', 'draw': '平局！', 'check': '将军！',
        'checkmate': '将死！', 'stalemate': '和棋！',
        'promotion': '兵的晋升', 'select_promo': '选择棋子：',
        'captured': '已吃子', 'undo': '悔棋', 'hint': '提示',
        'vs_ai': '对战AI', 'vs_human': '双人对战', 'mode': '模式',
        'ai_thinking': 'AI思考中...', 'no_moves': '没有有效移动',
        'queen': '后', 'rook': '车', 'bishop': '象', 'knight': '马',
    },
    'fa': {
        'title': 'بازی‌های رومیزی', 'chess': 'شطرنج', 'othello': 'اوتلو',
        'new_game': 'بازی جدید', 'quit': 'خروج', 'theme': 'پوسته',
        'lang': 'زبان', 'dark': 'تاریک', 'light': 'روشن',
        'white': 'سفید', 'black': 'سیاه', 'turn': 'نوبت',
        'score': 'امتیاز', 'pass_turn': 'رد کردن', 'game_over': 'پایان بازی',
        'wins': 'برنده شد!', 'draw': 'مساوی!', 'check': 'کیش!',
        'checkmate': 'کیش‌مات!', 'stalemate': 'بازی‌مات!',
        'promotion': 'ارتقای پیاده', 'select_promo': 'مهره انتخاب کنید:',
        'captured': 'خورده‌شده', 'undo': 'لغو', 'hint': 'راهنما',
        'vs_ai': 'در برابر هوش مصنوعی', 'vs_human': 'دو نفره', 'mode': 'حالت',
        'ai_thinking': 'هوش مصنوعی در حال فکر کردن...', 'no_moves': 'حرکتی وجود ندارد',
        'queen': 'وزیر', 'rook': 'رخ', 'bishop': 'فیل', 'knight': 'اسب',
    }
}

PIECE_UNICODE = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
}

INIT_BOARD = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['.','.','.','.','.','.','.','.',],
    ['.','.','.','.','.','.','.','.',],
    ['.','.','.','.','.','.','.','.',],
    ['.','.','.','.','.','.','.','.',],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R'],
]

class ChessEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [row[:] for row in INIT_BOARD]
        self.turn = 'white'
        self.castling = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant = None
        self.history = []
        self.captured_white = []
        self.captured_black = []
        self.status = 'playing'
        self.promotion_pending = None

    def is_white(self, p): return p != '.' and p.isupper()
    def is_black(self, p): return p != '.' and p.islower()
    def is_enemy(self, p, color): return (color == 'white' and self.is_black(p)) or (color == 'black' and self.is_white(p))
    def is_friend(self, p, color): return (color == 'white' and self.is_white(p)) or (color == 'black' and self.is_black(p))

    def in_bounds(self, r, c): return 0 <= r < 8 and 0 <= c < 8

    def raw_moves(self, r, c, board=None, en_passant=None, castling=None):
        if board is None: board = self.board
        if en_passant is None: en_passant = self.en_passant
        if castling is None: castling = self.castling
        p = board[r][c]
        if p == '.': return []
        color = 'white' if p.isupper() else 'black'
        pt = p.upper()
        moves = []

        def slide(dr, dc):
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc):
                if board[nr][nc] == '.':
                    moves.append((nr, nc))
                elif self.is_enemy(board[nr][nc], color):
                    moves.append((nr, nc)); break
                else: break
                nr += dr; nc += dc

        if pt == 'P':
            d = -1 if color == 'white' else 1
            sr = 6 if color == 'white' else 1
            if self.in_bounds(r+d, c) and board[r+d][c] == '.':
                moves.append((r+d, c))
                if r == sr and board[r+2*d][c] == '.':
                    moves.append((r+2*d, c))
            for dc in [-1, 1]:
                if self.in_bounds(r+d, c+dc):
                    if self.is_enemy(board[r+d][c+dc], color):
                        moves.append((r+d, c+dc))
                    elif en_passant == (r+d, c+dc):
                        moves.append((r+d, c+dc))
        elif pt == 'N':
            for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                nr, nc = r+dr, c+dc
                if self.in_bounds(nr, nc) and not self.is_friend(board[nr][nc], color):
                    moves.append((nr, nc))
        elif pt == 'B':
            for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]: slide(dr, dc)
        elif pt == 'R':
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]: slide(dr, dc)
        elif pt == 'Q':
            for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]: slide(dr, dc)
        elif pt == 'K':
            for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                nr, nc = r+dr, c+dc
                if self.in_bounds(nr, nc) and not self.is_friend(board[nr][nc], color):
                    moves.append((nr, nc))
            if color == 'white':
                if castling.get('K') and board[7][5]=='.' and board[7][6]=='.' and not self._sq_attacked(7,4,'black',board) and not self._sq_attacked(7,5,'black',board):
                    moves.append((7, 6))
                if castling.get('Q') and board[7][3]=='.' and board[7][2]=='.' and board[7][1]=='.' and not self._sq_attacked(7,4,'black',board) and not self._sq_attacked(7,3,'black',board):
                    moves.append((7, 2))
            else:
                if castling.get('k') and board[0][5]=='.' and board[0][6]=='.' and not self._sq_attacked(0,4,'white',board) and not self._sq_attacked(0,5,'white',board):
                    moves.append((0, 6))
                if castling.get('q') and board[0][3]=='.' and board[0][2]=='.' and board[0][1]=='.' and not self._sq_attacked(0,4,'white',board) and not self._sq_attacked(0,3,'white',board):
                    moves.append((0, 2))
        return moves

    def _sq_attacked(self, r, c, by_color, board=None):
        if board is None: board = self.board
        for rr in range(8):
            for cc in range(8):
                p = board[rr][cc]
                if p == '.': continue
                pc = 'white' if p.isupper() else 'black'
                if pc != by_color: continue
                mvs = self.raw_moves(rr, cc, board, en_passant=None, castling={'K':False,'Q':False,'k':False,'q':False})
                if (r, c) in mvs: return True
        return False

    def find_king(self, color, board=None):
        if board is None: board = self.board
        k = 'K' if color == 'white' else 'k'
        for r in range(8):
            for c in range(8):
                if board[r][c] == k: return r, c
        return None

    def in_check(self, color, board=None):
        if board is None: board = self.board
        kpos = self.find_king(color, board)
        if not kpos: return False
        enemy = 'black' if color == 'white' else 'white'
        return self._sq_attacked(kpos[0], kpos[1], enemy, board)

    def legal_moves(self, r, c):
        p = self.board[r][c]
        if p == '.': return []
        color = 'white' if p.isupper() else 'black'
        raw = self.raw_moves(r, c)
        legal = []
        for nr, nc in raw:
            nb = [row[:] for row in self.board]
            captured = nb[nr][nc]
            nb[nr][nc] = nb[r][c]
            nb[r][c] = '.'
            if p.upper() == 'P' and self.en_passant == (nr, nc):
                ep_r = r
                nb[ep_r][nc] = '.'
            if not self.in_check(color, nb):
                legal.append((nr, nc))
        return legal

    def all_legal_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p == '.': continue
                pc = 'white' if p.isupper() else 'black'
                if pc != color: continue
                for mv in self.legal_moves(r, c):
                    moves.append((r, c, mv[0], mv[1]))
        return moves

    def make_move(self, r, c, nr, nc):
        p = self.board[r][c]
        color = 'white' if p.isupper() else 'black'
        captured = self.board[nr][nc]
        snap = {
            'board': [row[:] for row in self.board],
            'turn': self.turn,
            'castling': dict(self.castling),
            'en_passant': self.en_passant,
            'captured_white': self.captured_white[:],
            'captured_black': self.captured_black[:],
        }
        self.history.append(snap)

        ep_captured = None
        if p.upper() == 'P' and self.en_passant == (nr, nc):
            ep_r = r
            ep_captured = self.board[ep_r][nc]
            self.board[ep_r][nc] = '.'

        self.board[nr][nc] = p
        self.board[r][c] = '.'

        if p.upper() == 'P' and abs(nr - r) == 2:
            self.en_passant = ((r + nr) // 2, c)
        else:
            self.en_passant = None

        if p == 'K':
            self.castling['K'] = False; self.castling['Q'] = False
            if nc == 6: self.board[7][5] = 'R'; self.board[7][7] = '.'
            elif nc == 2: self.board[7][3] = 'R'; self.board[7][0] = '.'
        elif p == 'k':
            self.castling['k'] = False; self.castling['q'] = False
            if nc == 6: self.board[0][5] = 'r'; self.board[0][7] = '.'
            elif nc == 2: self.board[0][3] = 'r'; self.board[0][0] = '.'
        elif p == 'R':
            if c == 7: self.castling['K'] = False
            elif c == 0: self.castling['Q'] = False
        elif p == 'r':
            if c == 7: self.castling['k'] = False
            elif c == 0: self.castling['q'] = False

        if captured != '.':
            if color == 'white': self.captured_white.append(captured)
            else: self.captured_black.append(captured)
        if ep_captured:
            if color == 'white': self.captured_white.append(ep_captured)
            else: self.captured_black.append(ep_captured)

        if p == 'P' and nr == 0:
            self.promotion_pending = (nr, nc, 'white')
        elif p == 'p' and nr == 7:
            self.promotion_pending = (nr, nc, 'black')
        else:
            self.promotion_pending = None
            self._finish_move(color)

    def promote(self, piece):
        if not self.promotion_pending: return
        nr, nc, color = self.promotion_pending
        self.board[nr][nc] = piece if color == 'white' else piece.lower()
        self.promotion_pending = None
        self._finish_move(color)

    def _finish_move(self, color):
        enemy = 'black' if color == 'white' else 'white'
        self.turn = enemy
        enemy_moves = self.all_legal_moves(enemy)
        if not enemy_moves:
            if self.in_check(enemy):
                self.status = 'checkmate'
            else:
                self.status = 'stalemate'
        elif self.in_check(enemy):
            self.status = 'check'
        else:
            self.status = 'playing'

    def undo(self):
        if not self.history: return
        snap = self.history.pop()
        self.board = snap['board']
        self.turn = snap['turn']
        self.castling = snap['castling']
        self.en_passant = snap['en_passant']
        self.captured_white = snap['captured_white']
        self.captured_black = snap['captured_black']
        self.status = 'playing'
        self.promotion_pending = None

    def ai_move(self):
        moves = self.all_legal_moves(self.turn)
        if not moves: return None
        import random
        best = None
        best_score = -99999
        color = self.turn
        for r, c, nr, nc in moves:
            nb = [row[:] for row in self.board]
            p = nb[r][c]
            cap = nb[nr][nc]
            nb[nr][nc] = p; nb[r][c] = '.'
            score = self._eval_board(nb, color)
            if cap != '.': score += self._piece_value(cap) * 10
            if score > best_score:
                best_score = score; best = (r, c, nr, nc)
        if best:
            r, c, nr, nc = best
            self.make_move(r, c, nr, nc)
            if self.promotion_pending:
                self.promote('Q')
        return best

    def _piece_value(self, p):
        vals = {'P':1,'N':3,'B':3,'R':5,'Q':9,'K':100}
        return vals.get(p.upper(), 0)

    def _eval_board(self, board, color):
        score = 0
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p == '.': continue
                v = self._piece_value(p)
                if (color == 'white' and p.isupper()) or (color == 'black' and p.islower()):
                    score += v
                else:
                    score -= v
        return score


class OthelloEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'; self.board[4][4] = 'W'
        self.board[3][4] = 'B'; self.board[4][3] = 'B'
        self.turn = 'B'
        self.status = 'playing'
        self.history = []
        self.passed = False

    def get_valid_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != '.': continue
                if self._can_place(r, c, color): moves.append((r, c))
        return moves

    def _can_place(self, r, c, color):
        opp = 'W' if color == 'B' else 'B'
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r+dr, c+dc
                found_opp = False
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == opp: found_opp = True
                    elif self.board[nr][nc] == color:
                        if found_opp: return True
                        break
                    else: break
                    nr += dr; nc += dc
        return False

    def make_move(self, r, c):
        color = self.turn
        opp = 'W' if color == 'B' else 'B'
        self.history.append([row[:] for row in self.board])
        self.board[r][c] = color
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                to_flip = []
                nr, nc = r+dr, c+dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == opp: to_flip.append((nr, nc))
                    elif self.board[nr][nc] == color:
                        for fr, fc in to_flip: self.board[fr][fc] = color
                        break
                    else: break
                    nr += dr; nc += dc
        next_color = opp
        if not self.get_valid_moves(next_color):
            if not self.get_valid_moves(color):
                self.status = 'gameover'
            else:
                self.turn = color
                self.status = 'passed'
                return
        else:
            self.turn = next_color
        self.status = 'playing'

    def undo(self):
        if not self.history: return
        self.board = self.history.pop()
        self.turn = 'W' if self.turn == 'B' else 'B'
        self.status = 'playing'

    def count(self):
        b = sum(row.count('B') for row in self.board)
        w = sum(row.count('W') for row in self.board)
        return b, w

    def winner(self):
        b, w = self.count()
        if b > w: return 'B'
        elif w > b: return 'W'
        return 'draw'

    def ai_move(self):
        moves = self.get_valid_moves(self.turn)
        if not moves: return None
        corners = [(0,0),(0,7),(7,0),(7,7)]
        for mv in moves:
            if mv in corners:
                self.make_move(*mv); return mv
        best = max(moves, key=lambda m: self._score_move(m[0], m[1]))
        self.make_move(*best)
        return best

    def _score_move(self, r, c):
        tmp = [row[:] for row in self.board]
        color = self.turn
        opp = 'W' if color == 'B' else 'B'
        tmp[r][c] = color
        score = 0
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0: continue
                to_flip = []
                nr, nc = r+dr, c+dc
                while 0<=nr<8 and 0<=nc<8:
                    if tmp[nr][nc]==opp: to_flip.append((nr,nc))
                    elif tmp[nr][nc]==color: score+=len(to_flip); break
                    else: break
                    nr+=dr; nc+=dc
        return score


class ChessBoard(QWidget):
    def __init__(self, theme, lang, mode='vs_human', parent=None):
        super().__init__(parent)
        self.theme = theme
        self.lang = lang
        self.mode = mode
        self.engine = ChessEngine()
        self.selected = None
        self.valid_moves = []
        self.hint_sq = None
        self.promo_dialog = None
        self.ai_timer = QTimer(self)
        self.ai_timer.setSingleShot(True)
        self.ai_timer.timeout.connect(self._do_ai)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def t(self, k): return TR[self.lang].get(k, k)

    def set_theme(self, theme): self.theme = theme; self.update()
    def set_lang(self, lang): self.lang = lang; self.update()
    def set_mode(self, mode): self.mode = mode; self.new_game()

    def new_game(self):
        self.engine.reset()
        self.selected = None
        self.valid_moves = []
        self.hint_sq = None
        self.update()

    def undo(self):
        if self.mode == 'vs_ai':
            self.engine.undo()
            if self.engine.history:
                self.engine.undo()
        else:
            self.engine.undo()
        self.selected = None
        self.valid_moves = []
        self.update()

    def cell_size(self):
        s = min(self.width(), self.height())
        return s / 8

    def cell_at(self, px, py):
        cs = self.cell_size()
        ox = (self.width() - cs * 8) / 2
        oy = (self.height() - cs * 8) / 2
        c = int((px - ox) / cs)
        r = int((py - oy) / cs)
        if 0 <= r < 8 and 0 <= c < 8: return r, c
        return None

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cs = self.cell_size()
        ox = (self.width() - cs * 8) / 2
        oy = (self.height() - cs * 8) / 2

        for r in range(8):
            for c in range(8):
                x, y = ox + c * cs, oy + r * cs
                is_light = (r + c) % 2 == 0
                col = QColor(self.theme['chess_light'] if is_light else self.theme['chess_dark'])
                p.fillRect(QRectF(x, y, cs, cs), col)

        border_pen = QPen(QColor(self.theme['chess_border']), max(2, cs * 0.04))
        p.setPen(border_pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(QRectF(ox, oy, cs * 8, cs * 8))

        for mv in self.valid_moves:
            vr, vc = mv
            x, y = ox + vc * cs, oy + vr * cs
            hl = QColor(self.theme['valid'])
            hl.setAlpha(120)
            p.fillRect(QRectF(x, y, cs, cs), hl)

        if self.selected:
            sr, sc = self.selected
            x, y = ox + sc * cs, oy + sr * cs
            sel = QColor(self.theme['selected'])
            sel.setAlpha(160)
            p.fillRect(QRectF(x, y, cs, cs), sel)

        if self.hint_sq:
            hr, hc = self.hint_sq
            x, y = ox + hc * cs, oy + hr * cs
            hint = QColor(self.theme['highlight'])
            hint.setAlpha(180)
            p.fillRect(QRectF(x, y, cs, cs), hint)

        king_pos = None
        if self.engine.status in ('check', 'checkmate'):
            kp = self.engine.find_king(self.engine.turn)
            if kp: king_pos = kp

        if king_pos:
            kr, kc = king_pos
            x, y = ox + kc * cs, oy + kr * cs
            danger = QColor('#e74c3c')
            danger.setAlpha(200)
            p.fillRect(QRectF(x, y, cs, cs), danger)

        for r in range(8):
            for c in range(8):
                piece = self.engine.board[r][c]
                if piece == '.': continue
                x, y = ox + c * cs, oy + r * cs
                sym = PIECE_UNICODE.get(piece, piece)
                fs = max(10, int(cs * 0.72))
                f = QFont('Segoe UI Symbol', fs)
                p.setFont(f)
                shadow = QColor(0, 0, 0, 80)
                p.setPen(shadow)
                p.drawText(QRectF(x+2, y+2, cs, cs), Qt.AlignmentFlag.AlignCenter, sym)
                tc = QColor('#f5f5f5') if piece.isupper() else QColor('#1a1a1a')
                p.setPen(tc)
                p.drawText(QRectF(x, y, cs, cs), Qt.AlignmentFlag.AlignCenter, sym)

        f_lbl = QFont('Arial', max(7, int(cs * 0.22)))
        p.setFont(f_lbl)
        for i in range(8):
            p.setPen(QColor(self.theme['sub']))
            p.drawText(QRectF(ox + i * cs, oy + cs * 8, cs, 14),
                       Qt.AlignmentFlag.AlignCenter, 'abcdefgh'[i])
            p.drawText(QRectF(ox - 14, oy + i * cs, 14, cs),
                       Qt.AlignmentFlag.AlignCenter, str(8 - i))

        status_txt = ''
        if self.engine.status == 'check': status_txt = self.t('check')
        elif self.engine.status == 'checkmate': status_txt = self.t('checkmate')
        elif self.engine.status == 'stalemate': status_txt = self.t('stalemate')
        if status_txt:
            f_st = QFont('Arial', max(12, int(cs * 0.4)), QFont.Weight.Black)
            p.setFont(f_st)
            p.setPen(QColor(self.theme['accent']))
            p.drawText(QRectF(ox, oy + cs * 8 + 16, cs * 8, 36),
                       Qt.AlignmentFlag.AlignCenter, status_txt)

        turn_col = '#f5f5f5' if self.engine.turn == 'white' else '#1a1a1a'
        p.setBrush(QColor(turn_col))
        p.setPen(QPen(QColor(self.theme['chess_border']), 1.5))
        ind = max(8, int(cs * 0.22))
        p.drawEllipse(QRectF(ox + cs * 8 + 6, oy, ind, ind))

        p.end()

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton: return
        if self.engine.status in ('checkmate', 'stalemate'): return
        if self.engine.promotion_pending: return
        if self.mode == 'vs_ai' and self.engine.turn == 'black': return

        cell = self.cell_at(e.position().x(), e.position().y())
        if not cell: return
        r, c = cell

        if self.selected:
            if (r, c) in self.valid_moves:
                self.engine.make_move(self.selected[0], self.selected[1], r, c)
                self.selected = None
                self.valid_moves = []
                if self.engine.promotion_pending:
                    self._show_promotion()
                elif self.mode == 'vs_ai' and self.engine.turn == 'black' and self.engine.status not in ('checkmate','stalemate'):
                    self.ai_timer.start(300)
                self.update()
                return
            else:
                self.selected = None
                self.valid_moves = []

        piece = self.engine.board[r][c]
        if piece == '.': self.update(); return
        color = 'white' if piece.isupper() else 'black'
        if color != self.engine.turn: self.update(); return
        self.selected = (r, c)
        self.valid_moves = self.engine.legal_moves(r, c)
        self.update()

    def _show_promotion(self):
        _, _, color = self.engine.promotion_pending
        pieces = ['Q', 'R', 'B', 'N'] if color == 'white' else ['q', 'r', 'b', 'n']
        names = [self.t('queen'), self.t('rook'), self.t('bishop'), self.t('knight')]
        d = QDialog(self)
        d.setWindowTitle(self.t('promotion'))
        d.setModal(True)
        lay = QVBoxLayout(d)
        lbl = QLabel(self.t('select_promo'))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(lbl)
        hl = QHBoxLayout()
        for p_char, p_name in zip(pieces, names):
            btn = QPushButton(f"{PIECE_UNICODE.get(p_char, p_char)}\n{p_name}")
            btn.setFixedSize(70, 70)
            btn.setFont(QFont('Segoe UI Symbol', 18))
            btn.clicked.connect(lambda _, pc=p_char: (self.engine.promote(pc), d.accept(), self.update(),
                                                      self.ai_timer.start(300) if self.mode=='vs_ai' and self.engine.turn=='black' else None))
            hl.addWidget(btn)
        lay.addLayout(hl)
        d.exec()

    def _do_ai(self):
        self.engine.ai_move()
        if self.engine.promotion_pending:
            self.engine.promote('Q')
        self.update()

    def hint(self):
        moves = self.engine.all_legal_moves(self.engine.turn)
        if moves:
            import random
            mv = random.choice(moves)
            self.hint_sq = (mv[0], mv[1])
            self.update()
            QTimer.singleShot(1500, lambda: (setattr(self, 'hint_sq', None), self.update()))


class OthelloBoard(QWidget):
    def __init__(self, theme, lang, mode='vs_human', parent=None):
        super().__init__(parent)
        self.theme = theme
        self.lang = lang
        self.mode = mode
        self.engine = OthelloEngine()
        self.valid_moves = []
        self.hover = None
        self.ai_timer = QTimer(self)
        self.ai_timer.setSingleShot(True)
        self.ai_timer.timeout.connect(self._do_ai)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._update_valid()

    def t(self, k): return TR[self.lang].get(k, k)
    def set_theme(self, theme): self.theme = theme; self.update()
    def set_lang(self, lang): self.lang = lang; self.update()
    def set_mode(self, mode): self.mode = mode; self.new_game()

    def new_game(self):
        self.engine.reset()
        self._update_valid()
        self.hover = None
        self.update()

    def undo(self):
        self.engine.undo()
        self._update_valid()
        self.update()

    def _update_valid(self):
        self.valid_moves = self.engine.get_valid_moves(self.engine.turn)

    def cell_size(self):
        s = min(self.width(), self.height())
        return s / 8

    def cell_at(self, px, py):
        cs = self.cell_size()
        ox = (self.width() - cs * 8) / 2
        oy = (self.height() - cs * 8) / 2
        c = int((px - ox) / cs)
        r = int((py - oy) / cs)
        if 0 <= r < 8 and 0 <= c < 8: return r, c
        return None

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cs = self.cell_size()
        ox = (self.width() - cs * 8) / 2
        oy = (self.height() - cs * 8) / 2

        for r in range(8):
            for c in range(8):
                x, y = ox + c * cs, oy + r * cs
                col = QColor(self.theme['board_dark'] if (r+c)%2==0 else self.theme['board_light'])
                p.fillRect(QRectF(x, y, cs, cs), col)

        p.setPen(QPen(QColor(self.theme['grid']), max(0.5, cs * 0.02)))
        for i in range(9):
            p.drawLine(QPointF(ox + i*cs, oy), QPointF(ox + i*cs, oy + 8*cs))
            p.drawLine(QPointF(ox, oy + i*cs), QPointF(ox + 8*cs, oy + i*cs))

        p.setPen(QPen(QColor(self.theme['board_border']), max(2, cs * 0.05)))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(QRectF(ox, oy, cs*8, cs*8))

        for r, c in self.valid_moves:
            x, y = ox + c*cs, oy + r*cs
            vc = QColor(self.theme['valid'])
            vc.setAlpha(70)
            p.fillRect(QRectF(x, y, cs, cs), vc)
            dot_c = QColor(self.theme['valid'])
            dot_c.setAlpha(150)
            p.setBrush(dot_c)
            p.setPen(Qt.PenStyle.NoPen)
            ds = cs * 0.18
            p.drawEllipse(QRectF(x + cs/2 - ds, y + cs/2 - ds, ds*2, ds*2))

        if self.hover and self.hover in self.valid_moves:
            hr, hc = self.hover
            x, y = ox + hc*cs, oy + hr*cs
            hv = QColor(self.theme['highlight'])
            hv.setAlpha(100)
            p.fillRect(QRectF(x, y, cs, cs), hv)

        dot_positions = [(2,2),(2,5),(5,2),(5,5)]
        for dr, dc in dot_positions:
            x, y = ox + dc*cs + cs/2, oy + dr*cs + cs/2
            p.setBrush(QColor(self.theme['board_border']))
            p.setPen(Qt.PenStyle.NoPen)
            ds = max(2, cs * 0.06)
            p.drawEllipse(QRectF(x-ds, y-ds, ds*2, ds*2))

        for r in range(8):
            for c in range(8):
                cell = self.engine.board[r][c]
                if cell == '.': continue
                x, y = ox + c*cs, oy + r*cs
                cx_, cy_ = x + cs/2, y + cs/2
                radius = cs * 0.40
                if cell == 'B':
                    grad = QRadialGradient(cx_ - radius*0.2, cy_ - radius*0.2, radius*1.2)
                    grad.setColorAt(0, QColor('#555'))
                    grad.setColorAt(1, QColor('#111'))
                    p.setBrush(grad)
                    p.setPen(QPen(QColor('#000'), max(1, cs*0.03)))
                else:
                    grad = QRadialGradient(cx_ - radius*0.2, cy_ - radius*0.2, radius*1.2)
                    grad.setColorAt(0, QColor('#fff'))
                    grad.setColorAt(1, QColor('#ccc'))
                    p.setBrush(grad)
                    p.setPen(QPen(QColor('#999'), max(1, cs*0.03)))
                p.drawEllipse(QRectF(cx_ - radius, cy_ - radius, radius*2, radius*2))

        bc, wc = self.engine.count()
        f = QFont('Arial', max(9, int(cs*0.3)), QFont.Weight.Bold)
        p.setFont(f)
        lh = max(20, int(cs*0.35))
        y_info = oy + cs*8 + 6
        p.setPen(QColor('#1a1a1a') if True else QColor('#fff'))
        p.setBrush(QColor('#111'))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QRectF(ox, y_info, lh*0.9, lh*0.9))
        p.setPen(QColor(self.theme['text']))
        p.drawText(QRectF(ox + lh, y_info, cs*2, lh), Qt.AlignmentFlag.AlignVCenter, f"{self.t('black')}: {bc}")
        p.setBrush(QColor('#eee'))
        p.setPen(QPen(QColor('#999'),1))
        p.drawEllipse(QRectF(ox + cs*4, y_info, lh*0.9, lh*0.9))
        p.setPen(QColor(self.theme['text']))
        p.drawText(QRectF(ox + cs*4 + lh, y_info, cs*2, lh), Qt.AlignmentFlag.AlignVCenter, f"{self.t('white')}: {wc}")

        if self.engine.status == 'gameover':
            winner = self.engine.winner()
            if winner == 'draw':
                txt = self.t('draw')
            else:
                wname = self.t('black') if winner == 'B' else self.t('white')
                txt = f"{wname} {self.t('wins')}"
            f2 = QFont('Arial', max(13, int(cs*0.45)), QFont.Weight.Black)
            p.setFont(f2)
            p.setPen(QColor(self.theme['accent']))
            p.drawText(QRectF(ox, y_info + lh + 4, cs*8, lh+10), Qt.AlignmentFlag.AlignCenter, txt)
        elif self.engine.status == 'passed':
            f2 = QFont('Arial', max(9, int(cs*0.28)))
            p.setFont(f2)
            p.setPen(QColor(self.theme['accent']))
            p.drawText(QRectF(ox, y_info + lh + 4, cs*8, lh), Qt.AlignmentFlag.AlignCenter, self.t('no_moves'))

        turn_x = ox + cs*8 + 6
        p.setBrush(QColor('#111') if self.engine.turn == 'B' else QColor('#eee'))
        border_c = QPen(QColor('#999' if self.engine.turn=='W' else '#333'), 1.5)
        p.setPen(border_c)
        ind = max(10, int(cs*0.28))
        p.drawEllipse(QRectF(turn_x, oy, ind, ind))

        p.end()

    def mouseMoveEvent(self, e):
        cell = self.cell_at(e.position().x(), e.position().y())
        self.hover = cell
        self.update()

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton: return
        if self.engine.status == 'gameover': return
        if self.mode == 'vs_ai' and self.engine.turn == 'W': return
        cell = self.cell_at(e.position().x(), e.position().y())
        if not cell: return
        r, c = cell
        if (r, c) not in self.valid_moves: return
        self.engine.make_move(r, c)
        self._update_valid()
        self.update()
        if self.mode == 'vs_ai' and self.engine.turn == 'W' and self.engine.status != 'gameover':
            self.ai_timer.start(400)

    def _do_ai(self):
        self.engine.ai_move()
        self._update_valid()
        self.update()

    def pass_turn(self):
        if self.engine.get_valid_moves(self.engine.turn): return
        self.engine.turn = 'W' if self.engine.turn == 'B' else 'B'
        self._update_valid()
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.current_lang = 'en'
        self.current_game = 'chess'
        self.current_mode = 'vs_human'
        self.setWindowTitle('Board Games')
        self.setMinimumSize(600, 520)
        self.resize(1000, 700)
        self._build_ui()
        self._apply_theme()

    def t(self, k): return TR[self.current_lang].get(k, k)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(50)
        tl = QHBoxLayout(self.top_bar)
        tl.setContentsMargins(12, 6, 12, 6)
        tl.setSpacing(10)

        self.title_lbl = QLabel(self.t('title'))
        self.title_lbl.setFont(QFont('Arial', 14, QFont.Weight.Black))
        tl.addWidget(self.title_lbl)
        tl.addSpacing(20)

        self.game_chess_btn = QPushButton(self.t('chess'))
        self.game_chess_btn.setCheckable(True)
        self.game_chess_btn.setChecked(True)
        self.game_chess_btn.clicked.connect(lambda: self._switch_game('chess'))
        tl.addWidget(self.game_chess_btn)

        self.game_othello_btn = QPushButton(self.t('othello'))
        self.game_othello_btn.setCheckable(True)
        self.game_othello_btn.clicked.connect(lambda: self._switch_game('othello'))
        tl.addWidget(self.game_othello_btn)

        tl.addStretch()

        self.mode_lbl = QLabel(self.t('mode') + ':')
        tl.addWidget(self.mode_lbl)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([self.t('vs_human'), self.t('vs_ai')])
        self.mode_combo.setFixedWidth(130)
        self.mode_combo.currentIndexChanged.connect(self._on_mode)
        tl.addWidget(self.mode_combo)

        self.lang_lbl = QLabel(self.t('lang') + ':')
        tl.addWidget(self.lang_lbl)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['English', '中文', 'فارسی'])
        self.lang_combo.setFixedWidth(90)
        self.lang_combo.currentIndexChanged.connect(self._on_lang)
        tl.addWidget(self.lang_combo)

        self.theme_lbl = QLabel(self.t('theme') + ':')
        tl.addWidget(self.theme_lbl)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([self.t('dark'), self.t('light')])
        self.theme_combo.setFixedWidth(80)
        self.theme_combo.currentIndexChanged.connect(self._on_theme)
        tl.addWidget(self.theme_combo)

        main_layout.addWidget(self.top_bar)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addWidget(content, stretch=1)

        self.chess_board = ChessBoard(THEMES[self.current_theme], self.current_lang, self.current_mode)
        self.othello_board = OthelloBoard(THEMES[self.current_theme], self.current_lang, self.current_mode)
        self.othello_board.setVisible(False)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.chess_board)
        self.stack.addWidget(self.othello_board)
        content_layout.addWidget(self.stack, stretch=1)

        self.side_panel = QWidget()
        self.side_panel.setFixedWidth(160)
        sp_layout = QVBoxLayout(self.side_panel)
        sp_layout.setContentsMargins(10, 16, 10, 16)
        sp_layout.setSpacing(10)
        sp_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.info_lbl = QLabel('')
        self.info_lbl.setWordWrap(True)
        self.info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_lbl.setFont(QFont('Arial', 10))
        sp_layout.addWidget(self.info_lbl)

        self.btn_new = self._btn(self.t('new_game'), self._do_new)
        self.btn_undo = self._btn(self.t('undo'), self._do_undo)
        self.btn_hint = self._btn(self.t('hint'), self._do_hint)
        self.btn_pass = self._btn(self.t('pass_turn'), self._do_pass)
        self.btn_quit = self._btn(self.t('quit'), self.close)

        for b in [self.btn_new, self.btn_undo, self.btn_hint, self.btn_pass, self.btn_quit]:
            sp_layout.addWidget(b)

        sp_layout.addStretch()

        self.captured_lbl = QLabel('')
        self.captured_lbl.setWordWrap(True)
        self.captured_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.captured_lbl.setFont(QFont('Segoe UI Symbol', 9))
        sp_layout.addWidget(self.captured_lbl)

        content_layout.addWidget(self.side_panel)

        self.bot_bar = QWidget()
        self.bot_bar.setFixedHeight(32)
        bl = QHBoxLayout(self.bot_bar)
        bl.setContentsMargins(12, 4, 12, 4)
        self.status_lbl = QLabel('')
        self.status_lbl.setFont(QFont('Arial', 10))
        bl.addWidget(self.status_lbl)
        bl.addStretch()
        main_layout.addWidget(self.bot_bar)

        self._update_side()

        upd_timer = QTimer(self)
        upd_timer.timeout.connect(self._refresh_info)
        upd_timer.start(500)

    def _btn(self, text, slot):
        b = QPushButton(text)
        b.setFixedHeight(36)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(slot)
        return b

    def _switch_game(self, game):
        self.current_game = game
        self.game_chess_btn.setChecked(game == 'chess')
        self.game_othello_btn.setChecked(game == 'othello')
        self.stack.setCurrentIndex(0 if game == 'chess' else 1)
        self._update_side()
        self._apply_theme()

    def _on_mode(self, idx):
        self.current_mode = ['vs_human', 'vs_ai'][idx]
        self.chess_board.set_mode(self.current_mode)
        self.othello_board.set_mode(self.current_mode)

    def _on_lang(self, idx):
        self.current_lang = ['en', 'zh', 'fa'][idx]
        self.chess_board.set_lang(self.current_lang)
        self.othello_board.set_lang(self.current_lang)
        self._update_texts()
        self._apply_theme()

    def _on_theme(self, idx):
        self.current_theme = 'dark' if idx == 0 else 'light'
        self.chess_board.set_theme(THEMES[self.current_theme])
        self.othello_board.set_theme(THEMES[self.current_theme])
        self._apply_theme()

    def _do_new(self):
        if self.current_game == 'chess': self.chess_board.new_game()
        else: self.othello_board.new_game()

    def _do_undo(self):
        if self.current_game == 'chess': self.chess_board.undo()
        else: self.othello_board.undo()

    def _do_hint(self):
        if self.current_game == 'chess': self.chess_board.hint()

    def _do_pass(self):
        if self.current_game == 'othello': self.othello_board.pass_turn()

    def _update_side(self):
        is_othello = self.current_game == 'othello'
        self.btn_hint.setVisible(not is_othello)
        self.btn_pass.setVisible(is_othello)

    def _refresh_info(self):
        if self.current_game == 'chess':
            e = self.chess_board.engine
            turn_txt = self.t('white') if e.turn == 'white' else self.t('black')
            self.info_lbl.setText(f"{self.t('turn')}: {turn_txt}")
            caps_w = ''.join(PIECE_UNICODE.get(p, p) for p in e.captured_white)
            caps_b = ''.join(PIECE_UNICODE.get(p, p) for p in e.captured_black)
            self.captured_lbl.setText(f"⬜{caps_w}\n⬛{caps_b}")
            st = e.status
            if st == 'check': self.status_lbl.setText(self.t('check'))
            elif st == 'checkmate': self.status_lbl.setText(self.t('checkmate'))
            elif st == 'stalemate': self.status_lbl.setText(self.t('stalemate'))
            else: self.status_lbl.setText('')
        else:
            e = self.othello_board.engine
            b, w = e.count()
            turn_name = self.t('black') if e.turn == 'B' else self.t('white')
            self.info_lbl.setText(f"{self.t('turn')}: {turn_name}\n⬛{b}  ⬜{w}")
            self.captured_lbl.setText('')
            if e.status == 'gameover':
                winner = e.winner()
                if winner == 'draw': self.status_lbl.setText(self.t('draw'))
                else:
                    wn = self.t('black') if winner == 'B' else self.t('white')
                    self.status_lbl.setText(f"{wn} {self.t('wins')}")
            else: self.status_lbl.setText('')

    def _update_texts(self):
        self.title_lbl.setText(self.t('title'))
        self.lang_lbl.setText(self.t('lang') + ':')
        self.theme_lbl.setText(self.t('theme') + ':')
        self.mode_lbl.setText(self.t('mode') + ':')
        self.game_chess_btn.setText(self.t('chess'))
        self.game_othello_btn.setText(self.t('othello'))
        self.btn_new.setText(self.t('new_game'))
        self.btn_undo.setText(self.t('undo'))
        self.btn_hint.setText(self.t('hint'))
        self.btn_pass.setText(self.t('pass_turn'))
        self.btn_quit.setText(self.t('quit'))
        self.mode_combo.blockSignals(True)
        self.mode_combo.clear()
        self.mode_combo.addItems([self.t('vs_human'), self.t('vs_ai')])
        self.mode_combo.setCurrentIndex(0 if self.current_mode == 'vs_human' else 1)
        self.mode_combo.blockSignals(False)
        self.theme_combo.blockSignals(True)
        self.theme_combo.clear()
        self.theme_combo.addItems([self.t('dark'), self.t('light')])
        self.theme_combo.setCurrentIndex(0 if self.current_theme == 'dark' else 1)
        self.theme_combo.blockSignals(False)

    def _apply_theme(self):
        th = THEMES[self.current_theme]
        checked_style = f"background-color: {th['accent']}; color: #fff; border: none;"
        qss = f"""
        QMainWindow, QWidget {{
            background-color: {th['bg']};
            color: {th['text']};
            font-family: Arial;
        }}
        QLabel {{ color: {th['text']}; background: transparent; }}
        QPushButton {{
            background-color: {th['btn']};
            color: {th['text']};
            border: 1px solid {th['border']};
            border-radius: 7px;
            padding: 5px 10px;
            font-weight: bold;
            font-size: 11px;
        }}
        QPushButton:hover {{
            background-color: {th['btn_hover']};
            color: #ffffff;
            border: 1px solid {th['accent']};
        }}
        QPushButton:pressed {{ background-color: {th['accent']}; color: #fff; }}
        QPushButton:checked {{ background-color: {th['accent']}; color: #fff; border: none; }}
        QComboBox {{
            background-color: {th['panel']};
            color: {th['text']};
            border: 1px solid {th['border']};
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 11px;
        }}
        QComboBox:hover {{ border: 1px solid {th['accent']}; }}
        QComboBox QAbstractItemView {{
            background-color: {th['panel']};
            color: {th['text']};
            selection-background-color: {th['btn_hover']};
            border: 1px solid {th['accent']};
        }}
        QComboBox::drop-down {{ border: none; width: 18px; }}
        QComboBox::down-arrow {{
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {th['text']};
            margin-right: 5px;
        }}
        QStackedWidget {{ background: {th['bg']}; }}
        """
        self.setStyleSheet(qss)
        bar_style = f"background-color: {th['panel']}; border-bottom: 1px solid {th['border']};"
        bot_style = f"background-color: {th['panel']}; border-top: 1px solid {th['border']};"
        side_style = f"background-color: {th['panel']}; border-left: 1px solid {th['border']};"
        self.top_bar.setStyleSheet(bar_style)
        self.bot_bar.setStyleSheet(bot_style)
        self.side_panel.setStyleSheet(side_style)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Board Games')
    app.setStyle('Fusion')

    font = QFont('Arial', 10)
    app.setFont(font)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
