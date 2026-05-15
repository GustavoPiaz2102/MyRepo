#!/usr/bin/env python3
"""
BIA — Interface Neural v4
pip install PySide6 requests
"""

import sys, math, json, requests
from pathlib import Path
from datetime import datetime

from PySide6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
	QTextEdit, QLineEdit, QLabel, QFrame, QSizePolicy,
	QListWidget, QListWidgetItem, QScrollArea
)
from PySide6.QtCore import (
	Qt, QTimer, QThread, Signal, QObject, QPointF, QRectF, QFile
)
from PySide6.QtGui import (
	QPainter, QColor, QPen, QFont,
	QRadialGradient, QLinearGradient,
	QPainterPath, QKeyEvent, QTextCursor, QPalette
)
from PySide6.QtUiTools import QUiLoader

# ─── Config ───────────────────────────────────────────────────────────────────
MODEL      = "bia"
OLLAMA_URL = "http://localhost:11434/api/chat"
HISTORY    = Path.home() / ".ollama_history.json"
UI_FILE    = Path(__file__).parent / "bia_layout.ui"

# ─── Paleta ───────────────────────────────────────────────────────────────────
BG      = QColor(4,    3,   1)
PANEL   = QColor(8,    6,   1)
PANEL2  = QColor(12,   9,   2)
BORDER  = QColor(35,  22,   3)
BORDER2 = QColor(55,  36,   6)
GOLD    = QColor(255, 185,   0)
GOLD2   = QColor(255, 210,  80)
ORANGE  = QColor(255, 115,   0)
EMBER   = QColor(255,  55,   0)
GLOW    = QColor(255, 250, 235)
DIM     = QColor(50,   32,   5)
DIM2    = QColor(90,   58,  10)
CYAN    = QColor(0,   200, 180)

# ─── Worker ───────────────────────────────────────────────────────────────────
import subprocess, re

MEMORY_FILE = Path.home() / ".relevantInformations.txt"


def _save_memory(content: str) -> str:
	try:
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
		line = f"[{timestamp}] {content}\n"
		with open(MEMORY_FILE, "a", encoding="utf-8") as f:
			f.write(line)
		return "ok"
	except Exception as e:
		return f"[erro: {e}]"

def _load_memory() -> str:
	"""Lê as informações salvas para injetar no contexto da IA."""
	if not MEMORY_FILE.exists():
		return ""
	try:
		with open(MEMORY_FILE, "r", encoding="utf-8") as f:
			return f.read().strip()
	except Exception as e:
		print(f"Erro ao carregar memória: {e}")
		return ""

def _run_shell(cmd: str) -> str:
	try:
		result = subprocess.run(
			cmd, shell=True, capture_output=True, text=True, timeout=15
		)
		out = (result.stdout + result.stderr).strip()
		if len(out) > 3000:
			out = out[:3000] + "\n[... output truncado ...]"
		return out if out else "(sem output)"
	except subprocess.TimeoutExpired:
		return "[erro: comando excedeu 15s]"
	except Exception as e:
		return f"[erro ao executar: {e}]"

def _parse_tool_call(text: str):
	"""Retorna (tool, payload) ou (None, None)."""
	text = text.strip()

	def _try(s):
		try:
			obj = json.loads(s)
			if not isinstance(obj, dict): return None
			tool = obj.get("tool")
			if tool == "shell"       and "cmd"     in obj: return ("shell",       obj["cmd"])
			if tool == "save_memory" and "content" in obj: return ("save_memory", obj["content"])
		except Exception:
			pass
		return None

	# 1. Resposta é só o JSON
	r = _try(text)
	if r: return r

	# 2. JSON embutido em texto
	for pat in [
		r'\{[^{}]*"tool"\s*:\s*"shell"[^{}]*\}',
		r'\{[^{}]*"tool"\s*:\s*"save_memory"[^{}]*\}',
		r'\{[^{}]*"cmd"\s*:\s*"[^"]*"[^{}]*\}',
	]:
		m = re.search(pat, text, re.DOTALL)
		if m:
			r = _try(m.group())
			if r: return r

	# 3. Bloco markdown
	m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
	if m:
		r = _try(m.group(1))
		if r: return r

	# 4. Fallback cmd solto
	m = re.search(r'"cmd"\s*:\s*"([^"]+)"', text)
	if m: return ("shell", m.group(1))

	return (None, None)


class OllamaWorker(QObject):
	finished     = Signal(str)
	error        = Signal(str)
	tool_called  = Signal(str, str)
	memory_saved = Signal(str)
	tokens_used  = Signal(int, int)    # (prompt_tokens, generated_tokens)

	def __init__(self, history):
		super().__init__()
		self.history = list(history)

	def run(self):
		try:
			for _ in range(8):
				# ── Injeta memória persistente no último prompt do usuário ──
				# Criamos uma cópia segura do histórico para não alterar a UI
				messages_to_send = [dict(m) for m in self.history] 
				memory_data = _load_memory()
				
				if memory_data and messages_to_send and messages_to_send[-1]["role"] == "user":
					original_content = messages_to_send[-1]["content"]
					messages_to_send[-1]["content"] = (
						"[CONTEXTO INTERNO — NUNCA REPITA ISSO NA RESPOSTA]\n"
						f"{memory_data}\n"
						"[FIM DO CONTEXTO INTERNO]\n"
						"Use essas informações acima para personalizar sua resposta. "
						"Jamais cite, liste, reproduza ou mencione este bloco de contexto.\n\n"
						f"{original_content}"
					)
				# ──────────────────────────────────────────────────────────────────

				resp = requests.post(
				OLLAMA_URL,
				json={
					"model": MODEL,
					"messages": messages_to_send,
					"stream": False,
					"options": {"num_ctx": 8192}
				},
				timeout=120,
				)


				resp.raise_for_status()
				data    = resp.json()
				content = data["message"]["content"]

				prompt_tok = data.get("prompt_eval_count", 0)
				gen_tok    = data.get("eval_count", 0)

				print(content)
				tool, payload = _parse_tool_call(content)

				if tool is None:
					self.tokens_used.emit(prompt_tok, gen_tok)
					self.finished.emit(content)
					return

				# ── save_memory ───────────────────────────────────────────────
				if tool == "save_memory":
					result = _save_memory(payload)
					self.memory_saved.emit(payload)
					self.history.append({"role": "assistant", "content": content})
					self.history.append({
						"role": "user",
						"content": f"[SISTEMA: Memória salva com sucesso: {result}] Continue."
					})
					continue

				# ── shell ─────────────────────────────────────────────────────
				output = _run_shell(payload)
				self.tool_called.emit(payload, output)
				self.history.append({"role": "assistant", "content": content})
				self.history.append({
					"role": "user",
					"content": (
						f"[TOOL OUTPUT]\n{output}\n[/TOOL OUTPUT]\n\n"
						"Analise o resultado acima e responda ao usuário final."
					)
				})

			self.finished.emit("[BIA: Limite de raciocínio recursivo atingido.]")

		except Exception as e:
			self.error.emit(f"Falha na Interface Neural: {str(e)}")


# ─── HUD ──────────────────────────────────────────────────────────────────────
class HUDWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.angle    = 0.0
		self.pulse    = 0.0
		self.thinking = False
		self._sparks  = []
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.setMinimumSize(300, 300)
		t = QTimer(self)
		t.timeout.connect(self._tick)
		t.start(28)

	def _tick(self):
		import random
		self.angle += 0.018
		self.pulse  = math.sin(self.angle * 2.8) * 0.5 + 0.5
		if random.random() < (0.15 if self.thinking else 0.04):
			a  = random.uniform(0, math.pi * 2)
			r  = random.uniform(0.72, 0.92)
			ml = random.randint(12, 30)
			self._sparks.append([a, r, ml, ml])
		for s in self._sparks:
			s[2] -= 1
		self._sparks = [s for s in self._sparks if s[2] > 0]
		self.update()

	def set_thinking(self, v):
		self.thinking = v

	def paintEvent(self, _):
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)
		p.setRenderHint(QPainter.SmoothPixmapTransform)
		w, h   = self.width(), self.height()
		cx, cy = w / 2.0, h / 2.0
		R      = min(w, h) * 0.44
		a      = self.angle
		pulse  = self.pulse

		# Fundo + vinheta
		p.fillRect(0, 0, w, h, BG)
		vgr = QRadialGradient(cx, cy, R * 1.7)
		vgr.setColorAt(0.0, QColor(20, 13, 2, 0))
		vgr.setColorAt(0.7, QColor(0,   0,  0, 0))
		vgr.setColorAt(1.0, QColor(0,   0,  0, 210))
		p.fillRect(0, 0, w, h, vgr)

		# Glow ambiental
		base_a = 22 if not self.thinking else 38
		amb = QRadialGradient(cx, cy, R * 1.3)
		amb.setColorAt(0.0, QColor(255, 130, 0, base_a + int(pulse * 18)))
		amb.setColorAt(0.5, QColor(200,  80, 0, (base_a + int(pulse * 18))//3))
		amb.setColorAt(1.0, QColor(0,     0, 0, 0))
		p.setBrush(amb); p.setPen(Qt.NoPen)
		p.drawEllipse(QPointF(cx, cy), R * 1.3, R * 1.3)

		# Scan lines
		p.setPen(QPen(QColor(0, 0, 0, 22), 1))
		for y in range(0, h, 3):
			p.drawLine(0, y, w, y)

		# Pontos decorativos externos
		for i in range(72):
			ang = i / 72 * math.pi * 2
			dot_a = int(35 + 28 * math.sin(ang * 3 + a * 0.5))
			p.setPen(Qt.NoPen)
			p.setBrush(QColor(120, 75, 10, dot_a))
			p.drawEllipse(
				QPointF(cx + math.cos(ang)*R*1.00, cy + math.sin(ang)*R*1.00),
				1.2, 1.2
			)

		# Anel 4 — arcos externos
		r4 = R * 0.94
		for i in range(48):
			frac = i / 48
			ang1 = frac * math.pi * 2 + a * 0.3
			ang2 = (frac + 1/48) * math.pi * 2 + a * 0.3
			wave = math.sin(frac * math.pi * 8 + a * 1.8)
			if wave < -0.4: continue
			t2 = max(0.0, wave)
			col = QColor(int(80+175*t2), int(45+60*t2), 0, int(50+140*t2))
			pen = QPen(col, 2.5); pen.setCapStyle(Qt.RoundCap)
			p.setPen(pen)
			p.drawArc(
				QRectF(cx-r4, cy-r4, r4*2, r4*2),
				int(-math.degrees(ang1)*16),
				int(-math.degrees(ang2-ang1)*16)
			)

		# Anel 3 — segmentos radiais
		r3i, r3o = R * 0.76, R * 0.88
		for i in range(40):
			frac     = i / 40
			base_ang = frac * math.pi * 2 + a * 0.55
			wave     = math.sin(frac * math.pi * 6 + a * 2.2)
			if wave < -0.2: continue
			intensity = max(0.0, wave)
			col = QColor(
				int(EMBER.red()  *0.3 + GOLD.red()  *0.7*intensity),
				int(EMBER.green()*0.3 + GOLD.green()*0.7*intensity),
				0, int(60+190*intensity)
			)
			pen = QPen(col, 2.6); pen.setCapStyle(Qt.RoundCap)
			p.setPen(pen); gap = 0.04
			p.drawLine(
				QPointF(cx+math.cos(base_ang+gap)*r3i, cy+math.sin(base_ang+gap)*r3i),
				QPointF(cx+math.cos(base_ang+gap)*r3o, cy+math.sin(base_ang+gap)*r3o),
			)
		p.setPen(QPen(QColor(80,50,5,60), 0.8)); p.setBrush(Qt.NoBrush)
		p.drawEllipse(QPointF(cx,cy), R*0.82, R*0.82)

		# Anel 2 — chevrons contra-rotativos
		r2 = R * 0.61
		for i in range(28):
			frac     = i / 28
			base_ang = frac * math.pi * 2 - a * 1.6
			wave     = math.cos(frac * math.pi * 5 - a * 3.2)
			if wave < 0.05: continue
			col = QColor(int(230+25*wave), int(140+45*wave), 0, int(50+200*wave))
			pen = QPen(col, 2.0); pen.setCapStyle(Qt.RoundCap)
			p.setPen(pen); span = 0.14
			path = QPainterPath()
			path.moveTo(cx+math.cos(base_ang-span)*(r2-6), cy+math.sin(base_ang-span)*(r2-6))
			path.lineTo(cx+math.cos(base_ang)*(r2+7),      cy+math.sin(base_ang)*(r2+7))
			path.lineTo(cx+math.cos(base_ang+span)*(r2-6), cy+math.sin(base_ang+span)*(r2-6))
			p.drawPath(path)
		p.setPen(QPen(QColor(100,65,8,55), 0.8)); p.setBrush(Qt.NoBrush)
		p.drawEllipse(QPointF(cx,cy), r2, r2)

		# Anel 1 — triângulos internos
		r1 = R * 0.38
		for i in range(14):
			frac     = i / 14
			base_ang = frac * math.pi * 2 + a * 3.0
			wave     = math.sin(frac * math.pi * 14 + a * 6)
			alpha    = int(60 + 195 * max(0.0, wave))
			p.setPen(Qt.NoPen)
			p.setBrush(QColor(255, int(50+40*max(0,wave)), 0, alpha))
			path = QPainterPath()
			path.moveTo(cx+math.cos(base_ang)*(r1+9),       cy+math.sin(base_ang)*(r1+9))
			path.lineTo(cx+math.cos(base_ang+0.22)*(r1-7),  cy+math.sin(base_ang+0.22)*(r1-7))
			path.lineTo(cx+math.cos(base_ang-0.22)*(r1-7),  cy+math.sin(base_ang-0.22)*(r1-7))
			path.closeSubpath()
			p.drawPath(path)
		p.setPen(QPen(QColor(80,50,5,50), 0.8)); p.setBrush(Qt.NoBrush)
		p.drawEllipse(QPointF(cx,cy), r1, r1)

		# Mira central
		p.setPen(QPen(QColor(255,185,0,60), 0.8))
		cl = R * 0.12
		p.drawLine(QPointF(cx-cl,cy), QPointF(cx+cl,cy))
		p.drawLine(QPointF(cx,cy-cl), QPointF(cx,cy+cl))

		# Faíscas
		for spark in self._sparks:
			sa, sr, sl2, sml = spark
			lf = sl2 / sml
			sx = cx + math.cos(sa) * sr * R
			sy = cy + math.sin(sa) * sr * R
			p.setPen(Qt.NoPen)
			p.setBrush(QColor(255, int(150*lf), 0, int(255*lf)))
			sz = 1.5 + 2.5*lf
			p.drawEllipse(QPointF(sx,sy), sz, sz)
			p.setPen(QPen(QColor(255,80,0,int(80*lf)), 0.8))
			ta = sa + math.pi
			p.drawLine(QPointF(sx,sy), QPointF(sx+math.cos(ta)*sz*3, sy+math.sin(ta)*sz*3))

		# Núcleo
		core_r = R * 0.19
		if self.thinking:
			for layer in range(5):
				lr   = core_r*(0.4+layer*0.28)*(0.82+0.18*pulse)
				bang = a*(3.5+layer*0.6)+layer*math.pi/2.5
				col  = QColor(255, int(30+layer*28), 0, int(220-layer*38))
				g = QRadialGradient(cx+math.cos(bang)*lr*0.35, cy+math.sin(bang)*lr*0.35, lr*1.1)
				g.setColorAt(0.0, col); g.setColorAt(1.0, QColor(0,0,0,0))
				p.setBrush(g); p.setPen(Qt.NoPen)
				p.drawEllipse(QPointF(cx,cy), lr, lr)
			ring_r = core_r*(0.9+0.15*pulse)
			p.setPen(QPen(QColor(255,0,0,int(120+80*pulse)), 1.5))
			p.setBrush(Qt.NoBrush)
			p.drawEllipse(QPointF(cx,cy), ring_r, ring_r)
		else:
			for layer in range(4):
				lr  = core_r*(1.0-layer*0.22)*(0.78+0.22*pulse)
				t2  = 1.0-layer/4.0
				col = QColor(255, int(230*t2+150*(1-t2)), int(180*t2), int(230*t2))
				g = QRadialGradient(cx, cy, lr)
				g.setColorAt(0.0, col)
				g.setColorAt(0.55, QColor(255,150,0,int(100*t2)))
				g.setColorAt(1.0,  QColor(0,0,0,0))
				p.setBrush(g); p.setPen(Qt.NoPen)
				p.drawEllipse(QPointF(cx,cy), lr, lr)
			cr = core_r*0.18*(0.9+0.1*pulse)
			cg = QRadialGradient(cx, cy, cr)
			cg.setColorAt(0.0, QColor(255,255,240,255))
			cg.setColorAt(1.0, QColor(255,220,100,0))
			p.setBrush(cg); p.setPen(Qt.NoPen)
			p.drawEllipse(QPointF(cx,cy), cr, cr)

		# Status label
		font = QFont("monospace", 8)
		font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
		font.setBold(True)
		p.setFont(font)
		if self.thinking:
			spin = "◜◝◞◟"[int(self.angle*12)%4]
			label = f"{spin}  PROCESSANDO  {spin}"
			p.setPen(QColor(255, 80, 0, 200))
		else:
			label = "◉   ONLINE"
			p.setPen(QColor(255, 185, 0, 180))
		p.drawText(QRectF(0, h-28, w, 22), Qt.AlignCenter, label)
		p.end()

# ─── Bubble Widget ────────────────────────────────────────────────────────────
class BubbleWidget(QWidget):
	"""Bolha individual de mensagem, alinhada à esquerda ou direita."""

	def __init__(self, text: str, role: str, parent=None):
		super().__init__(parent)
		self.role = role
		self._build(text)

	def _build(self, text: str):
		outer = QHBoxLayout(self)
		outer.setContentsMargins(40, 5, 40, 5)
		outer.setSpacing(0)

		if self.role == "system":
			lbl = QLabel(text)
			lbl.setAlignment(Qt.AlignCenter)
			lbl.setWordWrap(True)
			lbl.setStyleSheet(
				f"color:{DIM2.name()};font-family:monospace;font-size:10px;"
				f"letter-spacing:1px;padding:2px 0;"
			)
			outer.addWidget(lbl)
			return

		bubble = QLabel(text)
		bubble.setWordWrap(True)
		bubble.setTextFormat(Qt.RichText)
		bubble.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		bubble.setMinimumWidth(250)
		bubble.setMaximumWidth(750)

		if self.role == "user":
			bubble.setStyleSheet(
				f"color:{GLOW.name()};"
				f"background:rgba(255,185,0,0.12);"
				f"border:1px solid {GOLD.name()};"
				f"border-radius:15px 15px 2px 15px;"
				f"padding:12px 18px;"
				f"font-family:'JetBrains Mono','Fira Code',monospace;"
				f"font-size:13px;"
			)
			outer.addStretch(1)
			outer.addWidget(bubble)

		elif self.role == "bia":
			bubble.setStyleSheet(
				f"color:{GLOW.name()};"
				f"background:rgba(255,115,0,0.10);"
				f"border:1px solid {ORANGE.name()};"
				f"border-radius:15px 15px 15px 2px;"
				f"padding:12px 18px;"
				f"font-family:'JetBrains Mono','Fira Code',monospace;"
				f"font-size:13px;"
			)
			outer.addWidget(bubble)
			outer.addStretch(1)

		elif self.role == "error":
			bubble.setStyleSheet(
				f"color:{EMBER.name()}; border-left:2px solid {EMBER.name()};"
				f"padding:4px 10px; font-family:monospace; font-size:13px;"
			)
			outer.addWidget(bubble)
			outer.addStretch(1)

		elif self.role == "tool":
			bubble.setStyleSheet(
				f"color:{DIM2.name()}; background:rgba(255,185,0,0.04);"
				f"border:1px solid {BORDER2.name()}; border-left:2px solid {DIM2.name()};"
				f"border-radius:4px; padding:8px 16px; font-family:monospace; font-size:11px;"
			)
			outer.addSpacing(40); outer.addWidget(bubble); outer.addSpacing(40)

		elif self.role == "memory":
			bubble.setStyleSheet(
				f"color:{CYAN.name()}; background:rgba(0,200,180,0.05);"
				f"border:1px solid rgba(0,200,180,0.3); border-left:2px solid {CYAN.name()};"
				f"border-radius:4px; padding:6px 14px; font-family:monospace; font-size:10px;"
			)
			outer.addSpacing(60); outer.addWidget(bubble); outer.addSpacing(60)


class BubbleWithLabel(QWidget):
	"""Bolha + label de nome acima."""

	def __init__(self, text: str, role: str, parent=None):
		super().__init__(parent)
		layout = QVBoxLayout(self)
		layout.setContentsMargins(0, 5, 0, 15)
		layout.setSpacing(6)

		if role in ("user", "bia"):
			name_row = QHBoxLayout()
			name_row.setContentsMargins(45, 0, 45, 0)
			lbl_name = QLabel("▸ GUSTAVO" if role == "user" else "◈ BIA")
			lbl_name.setStyleSheet(
				f"color:{ GOLD.name() if role == 'user' else ORANGE.name() };"
				f"font-family:monospace; font-size:10px; font-weight:bold; letter-spacing:1.5px;"
			)
			if role == "user":
				name_row.addStretch()
				name_row.addWidget(lbl_name)
			else:
				name_row.addWidget(lbl_name)
				name_row.addStretch()
			layout.addLayout(name_row)

		layout.addWidget(BubbleWidget(text, role))


# ─── Chat Display ─────────────────────────────────────────────────────────────
class ChatDisplay(QListWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setFrameShape(QFrame.NoFrame)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setSpacing(2)
		self.setStyleSheet(f"""
			QListWidget {{
				background: transparent;
				border: none;
				outline: none;
			}}
			QListWidget::item {{
				background: transparent;
				border: none;
				padding: 0;
			}}
			QListWidget::item:selected {{
				background: transparent;
			}}
			QScrollBar:vertical {{
				background: transparent; width: 4px; border: none;
			}}
			QScrollBar::handle:vertical {{
				background: {DIM2.name()}; border-radius: 2px; min-height: 24px;
			}}
			QScrollBar::handle:vertical:hover {{ background: {GOLD.name()}; }}
			QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
			QScrollBar::add-page:vertical,  QScrollBar::sub-page:vertical {{ background:none; }}
		""")

	def _add(self, text: str, role: str):
		widget = BubbleWithLabel(text, role)
		widget.adjustSize()
		item = QListWidgetItem(self)
		item.setSizeHint(widget.sizeHint())
		self.addItem(item)
		self.setItemWidget(item, widget)
		self.scrollToBottom()

	def append_memory(self, content: str):
		self._add(f"◈ memória salva: {content}", "memory")

	def append_tool(self, cmd: str, output: str):
		lines = output.splitlines()
		preview = "\n".join(lines[:5])
		if len(lines) > 5:
			preview += f"\n... +{len(lines)-5} linhas"
		text = f"$ {cmd}\n{preview}"
		self._add(text, "tool")

	def append_user(self, text: str):
		self._add(text, "user")

	def append_bia(self, text: str):
		self._add(text, "bia")

	def append_system(self, text: str):
		self._add(text, "system")

	def append_error(self, text: str):
		self._add(f"✗ ERRO: {text}", "error")

	def clear(self):
		super().clear()


# ─── Input Bar ────────────────────────────────────────────────────────────────
class InputBar(QWidget):
	submitted = Signal(str)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setFixedHeight(56)
		layout = QHBoxLayout(self)
		layout.setContentsMargins(20, 10, 20, 10)
		layout.setSpacing(12)

		self.label = QLabel("GUSTAVO ›")
		self.label.setStyleSheet(
			f"color:{GOLD.name()};font-family:'JetBrains Mono','Fira Code',monospace;"
			f"font-size:12px;font-weight:bold;letter-spacing:2px;"
		)
		layout.addWidget(self.label)

		sep = QFrame()
		sep.setFrameShape(QFrame.VLine)
		sep.setFixedWidth(1)
		sep.setStyleSheet(f"background:{BORDER2.name()};")
		layout.addWidget(sep)

		self.field = QLineEdit()
		self.field.setFrame(False)
		self.field.setPlaceholderText("Digite sua mensagem...")
		self.field.setStyleSheet(f"""
			QLineEdit {{
				background:transparent; color:{GLOW.name()};
				font-family:'JetBrains Mono','Fira Code','Courier New',monospace;
				font-size:13px; border:none;
				selection-background-color:{GOLD.name()}; selection-color:#000;
			}}
		""")
		self.field.returnPressed.connect(self._submit)
		layout.addWidget(self.field)

		self.setStyleSheet(f"""
			InputBar {{ background:{PANEL2.name()}; border-top:1px solid {BORDER2.name()}; }}
		""")

	def _submit(self):
		t = self.field.text().strip()
		if t:
			self.submitted.emit(t)
			self.field.clear()

	def set_enabled(self, v):
		self.field.setEnabled(v)
		self.label.setStyleSheet(
			f"color:{GOLD.name() if v else DIM.name()};"
			f"font-family:'JetBrains Mono','Fira Code',monospace;"
			f"font-size:12px;font-weight:bold;letter-spacing:2px;"
		)

	def focus(self):
		self.field.setFocus()


# ─── Info Bar ─────────────────────────────────────────────────────────────────
class InfoBar(QWidget):
	NUM_CTX = 8192

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setFixedHeight(40)
		self._prompt_tok = 0
		self._gen_tok    = 0
		t = QTimer(self)
		t.timeout.connect(self.update)
		t.start(1000)

	def set_tokens(self, prompt_tok: int, gen_tok: int):
		self._prompt_tok = prompt_tok
		self._gen_tok    = gen_tok
		self.update()

	def paintEvent(self, _):
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)
		grad = QLinearGradient(0, 0, 0, self.height())
		grad.setColorAt(0.0, PANEL2); grad.setColorAt(1.0, PANEL)
		p.fillRect(self.rect(), grad)
		p.setPen(QPen(BORDER2, 1))
		p.drawLine(0, self.height()-1, self.width(), self.height()-1)
		p.setPen(QPen(QColor(GOLD.red(), GOLD.green(), GOLD.blue(), 55), 1))
		p.drawLine(0, self.height()-2, self.width(), self.height()-2)

		font = QFont("monospace", 9)
		font.setBold(True)
		font.setLetterSpacing(QFont.AbsoluteSpacing, 1.8)
		p.setFont(font)
		now = datetime.now()

		total_tok = self._prompt_tok + self._gen_tok
		pct       = total_tok / self.NUM_CTX if self.NUM_CTX else 0
		if pct < 0.6:
			tok_color = CYAN
		elif pct < 0.85:
			tok_color = GOLD
		else:
			tok_color = EMBER

		tok_str = f"{total_tok:,}/{self.NUM_CTX:,}" if total_tok else "─/─"

		items = [
			(GOLD,      "◈  BIA NEURAL INTERFACE"),
			(DIM2,      "    ·    "),
			(ORANGE,    "HORA "),   (GLOW,   now.strftime("%H:%M:%S")),
			(DIM2,      "    ·    "),
			(ORANGE,    "DATA "),   (GLOW,   now.strftime("%d/%m/%Y")),
			(DIM2,      "    ·    "),
			(ORANGE,    "MODELO "), (GLOW,   MODEL.upper()),
			(DIM2,      "    ·    "),
			(ORANGE,    "CTX "),    (tok_color, tok_str),
		]
		if total_tok:
			items += [
				(DIM2,   " ("),
				(ORANGE, "P "), (DIM2, f"{self._prompt_tok:,}"),
				(DIM2,   "  "),
				(ORANGE, "G "), (DIM2, f"{self._gen_tok:,}"),
				(DIM2,   ")"),
			]

		x = 16
		for col, txt in items:
			p.setPen(col); p.drawText(x, 26, txt)
			x += p.fontMetrics().horizontalAdvance(txt)

		if total_tok:
			bar_w = int(self.width() * min(pct, 1.0))
			bar_col = QColor(tok_color.red(), tok_color.green(), tok_color.blue(), 55)
			p.setPen(Qt.NoPen)
			p.setBrush(bar_col)
			p.drawRect(0, self.height()-2, bar_w, 2)

		p.end()


# ─── Janela Principal ─────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
	_reply_ready  = Signal(str)
	_error_ready  = Signal(str)
	_tool_ready   = Signal(str, str)
	_memory_ready = Signal(str)
	_tokens_ready = Signal(int, int)

	def __init__(self):
		super().__init__()
		self.history = self._load_history()

		loader = QUiLoader()
		loader.registerCustomWidget(HUDWidget)
		loader.registerCustomWidget(ChatDisplay)
		loader.registerCustomWidget(InputBar)
		loader.registerCustomWidget(InfoBar)

		qfile = QFile(str(UI_FILE))
		if not qfile.open(QFile.ReadOnly):
			raise RuntimeError(f"Não abriu {UI_FILE}")
		ui_container = loader.load(qfile)
		qfile.close()

		self.setCentralWidget(ui_container.centralwidget)
		self.setWindowTitle("BIA — Interface Neural")
		self.resize(1200, 740)

		self.hud       = self.findChild(HUDWidget,   "hud")
		self.chat      = self.findChild(ChatDisplay, "chat")
		self.input_bar = self.findChild(InputBar,    "input_bar")
		self.info_bar  = self.findChild(InfoBar,     "info_bar")

		self._apply_styles()
		self._reply_ready.connect(self._on_reply)
		self._error_ready.connect(self._on_error)
		self._tool_ready.connect(self._on_tool)
		self._memory_ready.connect(self._on_memory)
		self._tokens_ready.connect(self._on_tokens)
		self.input_bar.submitted.connect(self._on_submit)
		self._load_history_to_chat()
		self.input_bar.focus()

	def _apply_styles(self):
		self.setStyleSheet(f"QMainWindow {{ background:{BG.name()}; }}")
		lp = self.findChild(QWidget, "left_panel")
		if lp:
			lp.setStyleSheet(
				f"QWidget#left_panel {{"
				f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
				f"stop:0 {PANEL2.name()},stop:1 {PANEL.name()});"
				f"border-right:1px solid {BORDER2.name()};}}"
			)
		rp = self.findChild(QWidget, "right_panel")
		if rp:
			rp.setStyleSheet(f"QWidget#right_panel{{background:{BG.name()};}}")
		sl = self.findChild(QLabel, "shortcuts_label")
		if sl:
			sl.setStyleSheet(
				f"color:{DIM2.name()};font-family:monospace;font-size:10px;"
				f"letter-spacing:1px;padding:6px;"
				f"border-top:1px solid {BORDER.name()};background:{PANEL.name()};"
			)
		for name in ("top_separator", "input_separator"):
			f = self.findChild(QFrame, name)
			if f: f.setStyleSheet(f"background:{BORDER.name()};")

	def _load_history(self):
		return json.load(open(HISTORY)) if HISTORY.exists() else []

	def _save_history(self):
		json.dump(self.history, open(HISTORY, "w"))

	def _load_history_to_chat(self):
		self.chat.append_system("─ ─ ─  BIA NEURAL INTERFACE  ·  " + MODEL.upper() + "  ─ ─ ─")
		for msg in self.history[-10:]:
			if msg["role"] == "user": self.chat.append_user(msg["content"])
			else:                     self.chat.append_bia(msg["content"])
		if self.history:
			self.chat.append_system("─ ─ ─  sessão anterior  ─ ─ ─")

	def _on_submit(self, text: str):
		self.chat.append_user(text)
		self.history.append({"role": "user", "content": text})
		self.input_bar.set_enabled(False)
		self.hud.set_thinking(True)

		self.worker = OllamaWorker(self.history[-20:])
		self.thread = QThread()
		self.worker.moveToThread(self.thread)
		self.thread.started.connect(self.worker.run)
		self.worker.finished.connect(self._reply_ready.emit)
		self.worker.error.connect(self._error_ready.emit)
		self.worker.tool_called.connect(self._tool_ready.emit)
		self.worker.memory_saved.connect(self._memory_ready.emit)
		self.worker.tokens_used.connect(self._tokens_ready.emit)
		self.worker.finished.connect(self.thread.quit)
		self.worker.error.connect(self.thread.quit)
		self.thread.finished.connect(self.worker.deleteLater)
		self.thread.start()

	def _on_tokens(self, prompt_tok: int, gen_tok: int):
		if self.info_bar:
			self.info_bar.set_tokens(prompt_tok, gen_tok)

	def _on_tool(self, cmd: str, output: str):
		self.chat.append_tool(cmd, output)

	def _on_memory(self, content: str):
		self.chat.append_memory(content)

	def _on_reply(self, text: str):
		self.history.append({"role": "assistant", "content": text})
		self._save_history()
		self.chat.append_bia(text)
		self.input_bar.set_enabled(True)
		self.hud.set_thinking(False)
		self.input_bar.focus()

	def _on_error(self, err: str):
		self.chat.append_error(err)
		self.input_bar.set_enabled(True)
		self.hud.set_thinking(False)

	def keyPressEvent(self, e: QKeyEvent):
		if e.modifiers() == Qt.ControlModifier:
			if e.key() == Qt.Key_L:
				self.history = []; self._save_history(); self.chat.clear()
				self.chat.append_system("─ ─ ─  histórico limpo  ─ ─ ─")
				return
			if e.key() == Qt.Key_Q:
				self.close(); return
		super().keyPressEvent(e)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setApplicationName("BIA")
	palette = app.palette()
	palette.setColor(QPalette.Window,     BG)
	palette.setColor(QPalette.WindowText, GLOW)
	palette.setColor(QPalette.Base,       PANEL)
	palette.setColor(QPalette.Text,       GLOW)
	app.setPalette(palette)
	win = MainWindow()
	win.show()
	sys.exit(app.exec())