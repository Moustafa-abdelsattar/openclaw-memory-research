from manim import *
import numpy as np

# Color palette
LOBSTER_RED = "#E63946"
CLAUDE_ORANGE = "#E76F51"
ANTIGRAV_BLUE = "#457B9D"
DARK_BG = "#1D3557"
LIGHT_TEXT = "#F1FAEE"
ACCENT_GREEN = "#2A9D8F"
ACCENT_YELLOW = "#E9C46A"
SOFT_WHITE = "#F1FAEE"

class TitleScene(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # Lobster emoji
        lobster = Text("🦞", font_size=120)
        lobster.shift(UP * 0.5)

        title = Text("How AI Agents Remember", font_size=56, color=SOFT_WHITE, weight=BOLD)
        title.next_to(lobster, DOWN, buff=0.5)

        subtitle = Text(
            "OpenClaw  vs  Claude Code  vs  Antigravity",
            font_size=30, color=ACCENT_YELLOW
        )
        subtitle.next_to(title, DOWN, buff=0.4)

        byline = Text("Lobster Memory Research · March 2026", font_size=20, color=LIGHT_TEXT, opacity=0.6)
        byline.next_to(subtitle, DOWN, buff=0.6)

        self.play(FadeIn(lobster, scale=0.5), run_time=0.8)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(byline), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(Group(lobster, title, subtitle, byline), shift=UP), run_time=0.8)


class ProblemScene(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # Section header
        header = Text("The Core Problem", font_size=44, color=LOBSTER_RED, weight=BOLD)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=0.6)

        # Brain icon
        brain = Text("🧠", font_size=80)
        brain.shift(UP * 0.5)
        self.play(FadeIn(brain, scale=1.5), run_time=0.6)

        # Amnesia text
        amnesia = Text("AI models wake up with ZERO memory", font_size=32, color=SOFT_WHITE)
        amnesia.next_to(brain, DOWN, buff=0.5)
        self.play(Write(amnesia), run_time=0.8)
        self.wait(0.5)

        # Flash effect — brain fades
        self.play(brain.animate.set_opacity(0.2), run_time=0.3)
        self.play(brain.animate.set_opacity(1), run_time=0.3)
        self.play(brain.animate.set_opacity(0.2), run_time=0.3)

        forgot = Text("Every. Single. Session.", font_size=28, color=ACCENT_YELLOW)
        forgot.next_to(amnesia, DOWN, buff=0.4)
        self.play(FadeIn(forgot, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(Group(header, brain, amnesia, forgot)), run_time=0.6)


class ThreePhilosophies(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Three Tools, Three Philosophies", font_size=40, color=SOFT_WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.7)

        # Three columns
        col_data = [
            ("🦞", "OpenClaw", "Journal + Brain", LOBSTER_RED),
            ("🟠", "Claude Code", "Notepad per Project", CLAUDE_ORANGE),
            ("🚀", "Antigravity", "Knowledge Base", ANTIGRAV_BLUE),
        ]

        cards = VGroup()
        for i, (emoji, name, metaphor, color) in enumerate(col_data):
            card = VGroup()
            bg = RoundedRectangle(
                corner_radius=0.2, width=3.8, height=4,
                fill_color=color, fill_opacity=0.15,
                stroke_color=color, stroke_width=2
            )
            icon = Text(emoji, font_size=60)
            icon.move_to(bg.get_top() + DOWN * 0.7)
            label = Text(name, font_size=24, color=color, weight=BOLD)
            label.next_to(icon, DOWN, buff=0.3)
            desc = Text(metaphor, font_size=18, color=SOFT_WHITE)
            desc.next_to(label, DOWN, buff=0.3)
            card.add(bg, icon, label, desc)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.4)
        cards.next_to(header, DOWN, buff=0.6)

        for i, card in enumerate(cards):
            self.play(FadeIn(card, shift=UP * 0.5), run_time=0.5)
            self.wait(0.3)

        self.wait(2)
        self.play(FadeOut(Group(header, cards)), run_time=0.6)


class MemoryArchitecture(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Memory Architecture", font_size=40, color=LOBSTER_RED, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.6)

        # OpenClaw two-layer visualization
        oc_label = Text("OpenClaw — Two-Layer Memory", font_size=24, color=LOBSTER_RED, weight=BOLD)
        oc_label.next_to(header, DOWN, buff=0.5).shift(LEFT * 3)

        # Long-term memory box
        lt_box = RoundedRectangle(
            corner_radius=0.15, width=4.5, height=1.2,
            fill_color=LOBSTER_RED, fill_opacity=0.2,
            stroke_color=LOBSTER_RED, stroke_width=2
        )
        lt_text = Text("MEMORY.md", font_size=22, color=LOBSTER_RED, weight=BOLD)
        lt_desc = Text("Curated long-term wisdom", font_size=16, color=SOFT_WHITE)
        lt_group = VGroup(lt_text, lt_desc).arrange(DOWN, buff=0.1)
        lt_group.move_to(lt_box)
        lt_full = VGroup(lt_box, lt_group)

        # Daily memory box
        st_box = RoundedRectangle(
            corner_radius=0.15, width=4.5, height=1.2,
            fill_color=ACCENT_GREEN, fill_opacity=0.2,
            stroke_color=ACCENT_GREEN, stroke_width=2
        )
        st_text = Text("memory/YYYY-MM-DD.md", font_size=22, color=ACCENT_GREEN, weight=BOLD)
        st_desc = Text("Daily journal entries", font_size=16, color=SOFT_WHITE)
        st_group = VGroup(st_text, st_desc).arrange(DOWN, buff=0.1)
        st_group.move_to(st_box)
        st_full = VGroup(st_box, st_group)

        memory_stack = VGroup(lt_full, st_full).arrange(DOWN, buff=0.3)
        memory_stack.shift(LEFT * 3 + DOWN * 0.3)
        oc_label.next_to(memory_stack, UP, buff=0.3)

        # Claude Code hierarchy
        cc_label = Text("Claude Code — Project Memory", font_size=24, color=CLAUDE_ORANGE, weight=BOLD)

        cc_items = VGroup()
        for text, indent in [("~/.claude/CLAUDE.md (user)", 0), ("./CLAUDE.md (project)", 0.3), ("./CLAUDE.local.md (personal)", 0.6)]:
            item = Text(text, font_size=16, color=SOFT_WHITE)
            item.shift(RIGHT * indent)
            cc_items.add(item)
        cc_items.arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        cc_box = RoundedRectangle(
            corner_radius=0.15, width=4.5, height=2.5,
            fill_color=CLAUDE_ORANGE, fill_opacity=0.1,
            stroke_color=CLAUDE_ORANGE, stroke_width=2
        )
        cc_items.move_to(cc_box)
        cc_group = VGroup(cc_box, cc_items)
        cc_group.shift(RIGHT * 3 + DOWN * 0.3)
        cc_label.next_to(cc_group, UP, buff=0.3)

        self.play(FadeIn(oc_label), run_time=0.3)
        self.play(FadeIn(lt_full, shift=LEFT * 0.5), run_time=0.5)
        self.play(FadeIn(st_full, shift=LEFT * 0.5), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(cc_label), run_time=0.3)
        self.play(FadeIn(cc_group, shift=RIGHT * 0.5), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(Group(header, oc_label, memory_stack, cc_label, cc_group)), run_time=0.6)


class RetrievalScene(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Memory Retrieval", font_size=40, color=ACCENT_GREEN, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.6)

        # OpenClaw hybrid search diagram
        query_box = RoundedRectangle(
            corner_radius=0.15, width=3, height=0.8,
            fill_color=ACCENT_YELLOW, fill_opacity=0.3,
            stroke_color=ACCENT_YELLOW, stroke_width=2
        )
        query_text = Text("Search Query", font_size=18, color=ACCENT_YELLOW, weight=BOLD)
        query_text.move_to(query_box)
        query = VGroup(query_box, query_text)
        query.shift(UP * 2)

        # Two search paths
        vec_box = RoundedRectangle(
            corner_radius=0.15, width=3.2, height=1.2,
            fill_color=ANTIGRAV_BLUE, fill_opacity=0.2,
            stroke_color=ANTIGRAV_BLUE, stroke_width=2
        )
        vec_title = Text("Vector Search", font_size=18, color=ANTIGRAV_BLUE, weight=BOLD)
        vec_desc = Text("Semantic meaning", font_size=14, color=SOFT_WHITE)
        vec_group = VGroup(vec_title, vec_desc).arrange(DOWN, buff=0.1)
        vec_group.move_to(vec_box)
        vec = VGroup(vec_box, vec_group)
        vec.shift(LEFT * 2.5)

        bm25_box = RoundedRectangle(
            corner_radius=0.15, width=3.2, height=1.2,
            fill_color=LOBSTER_RED, fill_opacity=0.2,
            stroke_color=LOBSTER_RED, stroke_width=2
        )
        bm25_title = Text("BM25 Search", font_size=18, color=LOBSTER_RED, weight=BOLD)
        bm25_desc = Text("Exact keywords", font_size=14, color=SOFT_WHITE)
        bm25_group = VGroup(bm25_title, bm25_desc).arrange(DOWN, buff=0.1)
        bm25_group.move_to(bm25_box)
        bm25 = VGroup(bm25_box, bm25_group)
        bm25.shift(RIGHT * 2.5)

        # Merge box
        merge_box = RoundedRectangle(
            corner_radius=0.15, width=4, height=0.8,
            fill_color=ACCENT_GREEN, fill_opacity=0.3,
            stroke_color=ACCENT_GREEN, stroke_width=2
        )
        merge_text = Text("Weighted Merge (70/30)", font_size=18, color=ACCENT_GREEN, weight=BOLD)
        merge_text.move_to(merge_box)
        merge = VGroup(merge_box, merge_text)
        merge.shift(DOWN * 1)

        # Post-processing
        post_box = RoundedRectangle(
            corner_radius=0.15, width=5.5, height=0.8,
            fill_color=ACCENT_YELLOW, fill_opacity=0.2,
            stroke_color=ACCENT_YELLOW, stroke_width=2
        )
        post_text = Text("MMR Diversity + Temporal Decay → Results", font_size=16, color=ACCENT_YELLOW, weight=BOLD)
        post_text.move_to(post_box)
        post = VGroup(post_box, post_text)
        post.shift(DOWN * 2.2)

        # Arrows
        arr1 = Arrow(query_box.get_bottom(), vec_box.get_top(), buff=0.1, color=SOFT_WHITE, stroke_width=2)
        arr2 = Arrow(query_box.get_bottom(), bm25_box.get_top(), buff=0.1, color=SOFT_WHITE, stroke_width=2)
        arr3 = Arrow(vec_box.get_bottom(), merge_box.get_left() + UP * 0.1, buff=0.1, color=SOFT_WHITE, stroke_width=2)
        arr4 = Arrow(bm25_box.get_bottom(), merge_box.get_right() + UP * 0.1, buff=0.1, color=SOFT_WHITE, stroke_width=2)
        arr5 = Arrow(merge_box.get_bottom(), post_box.get_top(), buff=0.1, color=SOFT_WHITE, stroke_width=2)

        self.play(FadeIn(query, shift=DOWN * 0.3), run_time=0.5)
        self.play(GrowArrow(arr1), GrowArrow(arr2), run_time=0.5)
        self.play(FadeIn(vec, shift=DOWN * 0.3), FadeIn(bm25, shift=DOWN * 0.3), run_time=0.5)
        self.play(GrowArrow(arr3), GrowArrow(arr4), run_time=0.5)
        self.play(FadeIn(merge, shift=DOWN * 0.3), run_time=0.5)
        self.play(GrowArrow(arr5), run_time=0.4)
        self.play(FadeIn(post, shift=DOWN * 0.3), run_time=0.5)

        label = Text("OpenClaw's Hybrid Search — Most Sophisticated of the Three", font_size=18, color=ACCENT_YELLOW)
        label.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(label), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(Group(header, query, vec, bm25, merge, post, arr1, arr2, arr3, arr4, arr5, label)), run_time=0.6)


class MemoryFlushScene(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Pre-Compaction Memory Flush", font_size=38, color=LOBSTER_RED, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.6)

        subtitle = Text("OpenClaw's Unique Innovation", font_size=22, color=ACCENT_YELLOW)
        subtitle.next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=0.3)

        # Context window bar
        bar_bg = Rectangle(width=10, height=0.8, fill_color="#2B2B2B", fill_opacity=1, stroke_color=SOFT_WHITE, stroke_width=1)
        bar_bg.shift(UP * 0.5)

        bar_fill = Rectangle(width=7, height=0.76, fill_color=ACCENT_GREEN, fill_opacity=0.7, stroke_width=0)
        bar_fill.align_to(bar_bg, LEFT).shift(RIGHT * 0.02)
        bar_fill.move_to(bar_bg, aligned_edge=LEFT).shift(RIGHT * 0.02)

        bar_label = Text("Context Window", font_size=16, color=SOFT_WHITE)
        bar_label.next_to(bar_bg, UP, buff=0.15)

        pct = Text("70% full", font_size=16, color=SOFT_WHITE)
        pct.move_to(bar_bg)

        self.play(FadeIn(bar_bg), FadeIn(bar_label), run_time=0.3)
        self.play(GrowFromEdge(bar_fill, LEFT), FadeIn(pct), run_time=0.8)

        # Fill up the bar
        self.wait(0.5)
        self.play(
            bar_fill.animate.stretch_to_fit_width(8.5).align_to(bar_bg, LEFT).shift(RIGHT * 0.02),
            Transform(pct, Text("85% full", font_size=16, color=SOFT_WHITE).move_to(bar_bg)),
            run_time=0.8
        )

        # Warning zone
        self.play(
            bar_fill.animate.stretch_to_fit_width(9.2).align_to(bar_bg, LEFT).shift(RIGHT * 0.02).set_fill(ACCENT_YELLOW),
            Transform(pct, Text("92% — FLUSH TRIGGERED", font_size=16, color=DARK_BG, weight=BOLD).move_to(bar_bg)),
            run_time=0.8
        )

        # Steps
        steps = [
            "⚡ Silent turn fires automatically",
            "💾 Agent writes critical info to disk",
            "🤫 User sees nothing (NO_REPLY)",
            "🧹 Compaction proceeds safely",
        ]

        step_group = VGroup()
        for s in steps:
            t = Text(s, font_size=20, color=SOFT_WHITE)
            step_group.add(t)
        step_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        step_group.shift(DOWN * 1.5)

        for step in step_group:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.4)
            self.wait(0.3)

        insight = Text(
            '"Like writing notes before falling asleep"',
            font_size=20, color=ACCENT_YELLOW, slant=ITALIC
        )
        insight.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(insight), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(Group(header, subtitle, bar_bg, bar_fill, bar_label, pct, step_group, insight)), run_time=0.6)


class ComparisonMatrix(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Final Comparison", font_size=40, color=SOFT_WHITE, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=0.6)

        rows_data = [
            ("Memory Persistence", 5, 3, 4),
            ("Retrieval Power", 5, 3, 3),
            ("Multi-Channel", 5, 2, 2),
            ("Coding Ability", 4, 5, 5),
            ("Data Privacy", 5, 3, 3),
            ("Proactive Behavior", 5, 1, 3),
        ]

        all_items = VGroup()

        # Column headers
        hdr = VGroup(
            Text("Dimension", font_size=16, color=SOFT_WHITE, weight=BOLD),
            Text("🦞 OpenClaw", font_size=16, color=LOBSTER_RED, weight=BOLD),
            Text("🟠 Claude Code", font_size=16, color=CLAUDE_ORANGE, weight=BOLD),
            Text("🚀 Antigravity", font_size=16, color=ANTIGRAV_BLUE, weight=BOLD),
        )
        x_positions = [-3.5, -0.5, 2, 4.5]
        for j, item in enumerate(hdr):
            item.move_to([x_positions[j], 2, 0])
        all_items.add(hdr)
        self.play(FadeIn(hdr), run_time=0.4)

        row_vgroups = VGroup()
        for i, (label, oc, cc, ag) in enumerate(rows_data):
            y = 1.2 - i * 0.6
            row = VGroup()
            lbl = Text(label, font_size=15, color=SOFT_WHITE)
            lbl.move_to([x_positions[0], y, 0])
            row.add(lbl)

            for j, (score, color) in enumerate([(oc, LOBSTER_RED), (cc, CLAUDE_ORANGE), (ag, ANTIGRAV_BLUE)]):
                bar = Rectangle(
                    width=score * 0.3, height=0.25,
                    fill_color=color, fill_opacity=0.7, stroke_width=0
                )
                bar.move_to([x_positions[j + 1], y, 0])
                num = Text(str(score), font_size=14, color=SOFT_WHITE)
                num.next_to(bar, RIGHT, buff=0.1)
                row.add(bar, num)

            row_vgroups.add(row)
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.3)

        all_items.add(row_vgroups)
        self.wait(2)
        self.play(FadeOut(all_items), run_time=0.6)


class BottomLine(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("💡 Bottom Line", font_size=44, color=ACCENT_YELLOW, weight=BOLD)
        header.to_edge(UP, buff=0.8)
        self.play(Write(header), run_time=0.6)

        lines = [
            ("🦞 OpenClaw", "Best memory system — your always-on AI companion", LOBSTER_RED),
            ("🟠 Claude Code", "Best coding assistant — massive context, project-focused", CLAUDE_ORANGE),
            ("🚀 Antigravity", "Best autonomous IDE — agents that plan and verify", ANTIGRAV_BLUE),
        ]

        items = VGroup()
        for emoji_name, desc, color in lines:
            name = Text(emoji_name, font_size=26, color=color, weight=BOLD)
            description = Text(desc, font_size=20, color=SOFT_WHITE)
            item = VGroup(name, description).arrange(DOWN, buff=0.15)
            items.add(item)

        items.arrange(DOWN, buff=0.6)
        items.next_to(header, DOWN, buff=0.6)

        for item in items:
            self.play(FadeIn(item, shift=UP * 0.3), run_time=0.5)
            self.wait(0.4)

        # Final kicker
        kicker = Text(
            "They're not competitors — they're complementary.\nAnd OpenClaw can orchestrate them all. 🦞",
            font_size=22, color=ACCENT_YELLOW, weight=BOLD
        )
        kicker.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(kicker, scale=0.8), run_time=0.8)

        self.wait(2.5)
        self.play(FadeOut(Group(header, items, kicker)), run_time=0.8)


class LobsterMemoryVideo(Scene):
    """Full video — run all scenes in sequence."""
    def construct(self):
        scenes = [TitleScene, ProblemScene, ThreePhilosophies, MemoryArchitecture,
                   RetrievalScene, MemoryFlushScene, ComparisonMatrix, BottomLine]
        for SceneClass in scenes:
            s = SceneClass()
            s.camera = self.camera
            s.construct()
