/* ==========================================================================
   PERMANENT PROBLEM NOTES — JAVASCRIPT ENGINE & OFFLINE MARKDOWN RENDERER
   ========================================================================== */

let pnoteCurrentMode = 'read'; // 'read' | 'edit'
let pnoteEditorLayout = 'split'; // 'split' | 'write' | 'preview'
let isPnoteDirty = false;
let pnoteOriginalText = '';
let pnoteLivePreviewDebounce = null;

function escapeHtmlPnote(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
if (typeof escapeHtml !== 'function') {
  var escapeHtml = escapeHtmlPnote;
}

// 1. SYNTAX HIGHLIGHTING ENGINE (C++, Python, Java, SQL, JS, Bash)
const SyntaxHighlighter = {
  highlight(code, lang = 'cpp') {
    const l = (lang || '').toLowerCase().trim();
    if (l === 'cpp' || l === 'c++' || l === 'c' || l === 'h' || l === 'hpp') {
      return this.highlightCpp(code);
    } else if (l === 'python' || l === 'py') {
      return this.highlightPython(code);
    } else if (l === 'java') {
      return this.highlightJava(code);
    } else if (l === 'sql') {
      return this.highlightSql(code);
    } else if (l === 'javascript' || l === 'js' || l === 'ts' || l === 'typescript') {
      return this.highlightJs(code);
    } else if (l === 'bash' || l === 'sh' || l === 'zsh') {
      return this.highlightBash(code);
    }
    if (/\b(class|vector|cout|cin|unordered_map|public:|#include)\b/.test(code)) {
      return this.highlightCpp(code);
    }
    return escapeHtml(code);
  },

  highlightCpp(code) {
    const tokenRegex = /(\/\*[\s\S]*?\*\/|\/\/[^\r\n]*)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(^\s*#[a-zA-Z_]\w*(?:[^\r\n\\]|\\(?:\r\n|[\s\S]))*)|(\b0x[0-9a-fA-F]+|\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?:[uUlLfF]|ULL|LL)?\b)|(\b(?:class|struct|public|private|protected|virtual|override|final|int|long|double|float|char|bool|void|auto|const|static|constexpr|consteval|nullptr|NULL|return|if|else|for|while|do|switch|case|break|continue|new|delete|this|sizeof|typedef|using|namespace|template|typename|try|catch|throw|inline|explicit|friend|default|enum|operator|static_cast|dynamic_cast|reinterpret_cast|const_cast)\b)|(\b(?:std|vector|string|unordered_map|map|unordered_set|set|pair|queue|priority_queue|stack|deque|list|array|bitset|tuple|iterator|size_t|int64_t|uint64_t|int32_t|uint32_t|stringstream|cin|cout|cerr|endl|numeric_limits|min|max|sort|reverse|swap|make_pair|make_tuple|push_back|emplace_back|pop_back|push|pop|top|front|back|size|empty|clear|insert|erase|find|count|begin|end|rbegin|rend|lower_bound|upper_bound|binary_search|accumulate|INT_MAX|INT_MIN|LLONG_MAX|LLONG_MIN)\b)|(->|::|\+\+|--|<=|>=|==|!=|&&|\|\||<<|>>|[+\-*/%=&|^~<>!?:]+)/gm;

    let result = '';
    let lastIndex = 0;
    let match;

    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) {
        result += escapeHtml(code.slice(lastIndex, match.index));
      }
      const [full, comment, string, macro, number, keyword, type, op] = match;
      if (comment) result += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
      else if (string) result += `<span class="tok-string">${escapeHtml(string)}</span>`;
      else if (macro) result += `<span class="tok-macro">${escapeHtml(macro)}</span>`;
      else if (number) result += `<span class="tok-num">${escapeHtml(number)}</span>`;
      else if (keyword) result += `<span class="tok-kw">${escapeHtml(keyword)}</span>`;
      else if (type) result += `<span class="tok-type">${escapeHtml(type)}</span>`;
      else if (op) result += `<span class="tok-op">${escapeHtml(op)}</span>`;
      else result += escapeHtml(full);
      lastIndex = tokenRegex.lastIndex;
    }
    if (lastIndex < code.length) result += escapeHtml(code.slice(lastIndex));
    return result;
  },

  highlightPython(code) {
    const tokenRegex = /(#[^\r\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b\d+(?:\.\d+)?\b)|(\b(?:def|class|return|if|elif|else|for|while|break|continue|in|not|and|or|is|import|from|as|try|except|finally|raise|with|yield|lambda|pass|global|nonlocal|async|await)\b)|(\b(?:self|None|True|False|print|len|range|enumerate|zip|map|filter|int|float|str|list|dict|set|tuple|bool|min|max|sum|sorted|open|isinstance)\b)|(<=|>=|==|!=|\+=|-=|\*=|\/=|->|[+\-*/%=&|^~<>]+)/g;
    let result = '', lastIndex = 0, match;
    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) result += escapeHtml(code.slice(lastIndex, match.index));
      const [full, comment, string, number, keyword, builtIn, op] = match;
      if (comment) result += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
      else if (string) result += `<span class="tok-string">${escapeHtml(string)}</span>`;
      else if (number) result += `<span class="tok-num">${escapeHtml(number)}</span>`;
      else if (keyword) result += `<span class="tok-kw">${escapeHtml(keyword)}</span>`;
      else if (builtIn) result += `<span class="tok-type">${escapeHtml(builtIn)}</span>`;
      else if (op) result += `<span class="tok-op">${escapeHtml(op)}</span>`;
      else result += escapeHtml(full);
      lastIndex = tokenRegex.lastIndex;
    }
    if (lastIndex < code.length) result += escapeHtml(code.slice(lastIndex));
    return result;
  },

  highlightJava(code) {
    const tokenRegex = /(\/\*[\s\S]*?\*\/|\/\/[^\r\n]*)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b\d+(?:\.\d+)?(?:[fFdDlL])?\b)|(\b(?:public|private|protected|class|interface|extends|implements|static|final|abstract|void|int|long|double|float|char|boolean|byte|short|new|return|if|else|for|while|do|switch|case|break|continue|try|catch|finally|throw|throws|import|package|this|super|null|true|false|instanceof|synchronized)\b)|(\b(?:String|Integer|Long|Double|Boolean|List|ArrayList|LinkedList|Map|HashMap|TreeMap|Set|HashSet|TreeSet|Queue|Deque|PriorityQueue|Stack|Arrays|Collections|Math|System|Override)\b)|(->|\+\+|--|<=|>=|==|!=|&&|\|\||[+\-*/%=&|^~<>!?:]+)/g;
    let result = '', lastIndex = 0, match;
    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) result += escapeHtml(code.slice(lastIndex, match.index));
      const [full, comment, string, number, keyword, type, op] = match;
      if (comment) result += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
      else if (string) result += `<span class="tok-string">${escapeHtml(string)}</span>`;
      else if (number) result += `<span class="tok-num">${escapeHtml(number)}</span>`;
      else if (keyword) result += `<span class="tok-kw">${escapeHtml(keyword)}</span>`;
      else if (type) result += `<span class="tok-type">${escapeHtml(type)}</span>`;
      else if (op) result += `<span class="tok-op">${escapeHtml(op)}</span>`;
      else result += escapeHtml(full);
      lastIndex = tokenRegex.lastIndex;
    }
    if (lastIndex < code.length) result += escapeHtml(code.slice(lastIndex));
    return result;
  },

  highlightSql(code) {
    const tokenRegex = /(--[^\r\n]*|\/\*[\s\S]*?\*\/)|('(?:''|[^'])*')|(\b\d+(?:\.\d+)?\b)|(\b(?:SELECT|FROM|WHERE|GROUP\s+BY|HAVING|ORDER\s+BY|LIMIT|OFFSET|JOIN|LEFT\s+JOIN|RIGHT\s+JOIN|INNER\s+JOIN|OUTER\s+JOIN|CROSS\s+JOIN|ON|AS|AND|OR|NOT|IN|BETWEEN|LIKE|IS\s+NULL|IS\s+NOT\s+NULL|COUNT|SUM|AVG|MIN|MAX|DISTINCT|CASE|WHEN|THEN|ELSE|END|OVER|PARTITION\s+BY|ROW_NUMBER|RANK|DENSE_RANK|UNION|ALL|INSERT\s+INTO|VALUES|UPDATE|SET|DELETE|CREATE\s+TABLE|DROP\s+TABLE|ALTER\s+TABLE|PRIMARY\s+KEY|FOREIGN\s+KEY|NULL|TRUE|FALSE|DESC|ASC|WITH|COALESCE|CONCAT)\b)/gi;
    let result = '', lastIndex = 0, match;
    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) result += escapeHtml(code.slice(lastIndex, match.index));
      const [full, comment, string, number, keyword] = match;
      if (comment) result += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
      else if (string) result += `<span class="tok-string">${escapeHtml(string)}</span>`;
      else if (number) result += `<span class="tok-num">${escapeHtml(number)}</span>`;
      else if (keyword) result += `<span class="tok-kw">${escapeHtml(keyword.toUpperCase())}</span>`;
      else result += escapeHtml(full);
      lastIndex = tokenRegex.lastIndex;
    }
    if (lastIndex < code.length) result += escapeHtml(code.slice(lastIndex));
    return result;
  },

  highlightJs(code) {
    const tokenRegex = /(\/\*[\s\S]*?\*\/|\/\/[^\r\n]*)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)|(\b\d+(?:\.\d+)?\b)|(\b(?:const|let|var|function|return|if|else|for|while|do|switch|case|break|continue|try|catch|finally|throw|new|this|class|extends|super|import|export|from|default|async|await|typeof|instanceof|null|undefined|true|false)\b)|(\b(?:Array|Object|String|Number|Boolean|Map|Set|Promise|console|Math|JSON)\b)|(=>|===|!==|<=|>=|&&|\|\||[+\-*/%=&|^~<>!?:]+)/g;
    let result = '', lastIndex = 0, match;
    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) result += escapeHtml(code.slice(lastIndex, match.index));
      const [full, comment, string, number, keyword, type, op] = match;
      if (comment) result += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
      else if (string) result += `<span class="tok-string">${escapeHtml(string)}</span>`;
      else if (number) result += `<span class="tok-num">${escapeHtml(number)}</span>`;
      else if (keyword) result += `<span class="tok-kw">${escapeHtml(keyword)}</span>`;
      else if (type) result += `<span class="tok-type">${escapeHtml(type)}</span>`;
      else if (op) result += `<span class="tok-op">${escapeHtml(op)}</span>`;
      else result += escapeHtml(full);
      lastIndex = tokenRegex.lastIndex;
    }
    if (lastIndex < code.length) result += escapeHtml(code.slice(lastIndex));
    return result;
  },

  highlightBash(code) {
    const tokenRegex = /(#[^\r\n]*)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b(?:echo|cd|ls|grep|sed|awk|cat|curl|wget|chmod|chown|export|source|npm|node|python|python3|git|mkdir|rm|cp|mv|sudo|if|then|else|elif|fi|for|do|done|while|case|esac|function)\b)|(\$[a-zA-Z_]\w*|\$\{[^}]+\})/g;
    let result = '', lastIndex = 0, match;
    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) result += escapeHtml(code.slice(lastIndex, match.index));
      const [full, comment, string, keyword, variable] = match;
      if (comment) result += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
      else if (string) result += `<span class="tok-string">${escapeHtml(string)}</span>`;
      else if (keyword) result += `<span class="tok-kw">${escapeHtml(keyword)}</span>`;
      else if (variable) result += `<span class="tok-type">${escapeHtml(variable)}</span>`;
      else result += escapeHtml(full);
      lastIndex = tokenRegex.lastIndex;
    }
    if (lastIndex < code.length) result += escapeHtml(code.slice(lastIndex));
    return result;
  }
};

// 2. OFFLINE MARKDOWN RENDERER
function renderMarkdownToHtml(rawMarkdown) {
  if (!rawMarkdown || !rawMarkdown.trim()) {
    return '<div class="pnote-empty-state"><div style="font-size:2rem; margin-bottom:0.75rem;">📝</div><div>No notes written yet. Click <b>Edit Notes</b> to write or paste technical notes from ChatGPT.</div></div>';
  }

  // Sanitize dangerous raw tags before parsing
  let text = rawMarkdown.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  text = text.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
  text = text.replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '');

  const codeBlocks = [];
  const mathBlocks = [];

  // Extract fenced code blocks
  text = text.replace(/```([a-zA-Z0-9_\-+]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    const id = codeBlocks.length;
    codeBlocks.push({ lang: lang.trim(), code: code });
    return `@@@PNOTECODEBLOCK${id}@@@`;
  });

  // Extract display math ($$...$$)
  text = text.replace(/\$\$([\s\S]*?)\$\$/g, (match, formula) => {
    const id = mathBlocks.length;
    mathBlocks.push({ display: true, formula: formula.trim() });
    return `@@@PNOTEMATHBLOCK${id}@@@`;
  });

  // Extract inline math ($...$)
  text = text.replace(/(^|[^\\])\$([^\$\n]+?)\$/g, (match, prefix, formula) => {
    const id = mathBlocks.length;
    mathBlocks.push({ display: false, formula: formula.trim() });
    return `${prefix}@@@PNOTEMATHBLOCK${id}@@@`;
  });

  const lines = text.split('\n');
  const output = [];
  let listLines = [];
  let inBlockquote = false;
  let blockquoteLines = [];
  let inTable = false;
  let tableRows = [];

  const flushList = () => {
    if (listLines.length === 0) return;
    output.push(parseListBlock(listLines));
    listLines = [];
  };

  const flushBlockquote = () => {
    if (!inBlockquote) return;
    const fullText = blockquoteLines.join('\n');
    let calloutType = 'note';
    let calloutIcon = '💡';
    let calloutTitle = 'Note';
    let bodyText = fullText;

    const bLines = fullText.split('\n');
    const firstMatch = bLines[0].trim().match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](?:\s+(.*))?$/i);
    if (firstMatch) {
      const type = firstMatch[1].toUpperCase();
      const customTitle = firstMatch[2] ? firstMatch[2].trim() : null;
      bodyText = bLines.slice(1).join('\n').trim();
      if (type === 'NOTE') { calloutType = 'note'; calloutIcon = '📘'; calloutTitle = customTitle || 'Note'; }
      else if (type === 'TIP') { calloutType = 'tip'; calloutIcon = '💡'; calloutTitle = customTitle || 'Key Idea / Tip'; }
      else if (type === 'IMPORTANT') { calloutType = 'important'; calloutIcon = '⭐'; calloutTitle = customTitle || 'Important'; }
      else if (type === 'WARNING') { calloutType = 'warning'; calloutIcon = '⚠️'; calloutTitle = customTitle || 'Warning / Caution'; }
      else if (type === 'CAUTION') { calloutType = 'danger'; calloutIcon = '🚨'; calloutTitle = customTitle || 'Edge Case'; }
    } else if (/^\*\*(?:Key\s*Idea|Idea|Invariant|Intuition|Crux):\*\*/i.test(fullText)) {
      calloutType = 'tip';
      calloutIcon = '💡';
      calloutTitle = 'Key Idea / Invariant';
    }

    const renderedBody = parseInlineMarkdown(bodyText.replace(/\n/g, '<br>'));
    output.push(`
      <div class="pnote-callout pnote-callout-${calloutType}">
        <div class="pnote-callout-header">
          <span class="pnote-callout-icon">${calloutIcon}</span>
          <span class="pnote-callout-title">${calloutTitle}</span>
        </div>
        <div class="pnote-callout-body">${renderedBody}</div>
      </div>
    `);
    inBlockquote = false;
    blockquoteLines = [];
  };

  const flushTable = () => {
    if (!inTable) return;
    if (tableRows.length < 2) {
      tableRows.forEach(r => output.push(`<p class="pnote-p">${parseInlineMarkdown(r)}</p>`));
      inTable = false;
      tableRows = [];
      return;
    }

    const headerLine = tableRows[0];
    const alignLine = tableRows[1];
    const dataLines = tableRows.slice(2);

    const parseCells = (line) => line.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());

    const headers = parseCells(headerLine);
    const aligns = parseCells(alignLine).map(a => {
      if (/^:---+:$/.test(a)) return 'center';
      if (/^---+:$/.test(a)) return 'right';
      return 'left';
    });

    let tableHtml = '<div class="pnote-table-wrap"><table class="pnote-table"><thead><tr>';
    headers.forEach((h, idx) => {
      const align = aligns[idx] || 'left';
      tableHtml += `<th style="text-align:${align};">${parseInlineMarkdown(h)}</th>`;
    });
    tableHtml += '</tr></thead><tbody>';

    dataLines.forEach(rowLine => {
      const cells = parseCells(rowLine);
      tableHtml += '<tr>';
      headers.forEach((_, idx) => {
        const val = cells[idx] || '';
        const align = aligns[idx] || 'left';
        tableHtml += `<td style="text-align:${align};">${parseInlineMarkdown(val)}</td>`;
      });
      tableHtml += '</tr>';
    });

    tableHtml += '</tbody></table></div>';
    output.push(tableHtml);
    inTable = false;
    tableRows = [];
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // Table rows
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      flushList();
      flushBlockquote();
      inTable = true;
      tableRows.push(trimmed);
      continue;
    } else if (inTable) {
      flushTable();
    }

    // Blockquote
    if (trimmed.startsWith('>')) {
      flushList();
      inBlockquote = true;
      blockquoteLines.push(trimmed.replace(/^>\s?/, ''));
      continue;
    } else if (inBlockquote) {
      flushBlockquote();
    }

    // List item detection
    const isListItem = /^\s*([\-*+]|\d+\.)\s+/.test(line);
    const isIndentedListContinuation = listLines.length > 0 && /^\s{2,}/.test(line) && trimmed.length > 0;

    if (isListItem || isIndentedListContinuation) {
      listLines.push(line);
      continue;
    } else if (listLines.length > 0) {
      flushList();
    }

    // Horizontal Rule
    if (/^(\-{3,}|\*{3,}|_{3,})$/.test(trimmed)) {
      output.push('<hr class="pnote-hr">');
      continue;
    }

    // Headings
    const h1Match = trimmed.match(/^#\s+(.*)$/);
    if (h1Match) { output.push(`<h1 class="pnote-h1">${parseInlineMarkdown(h1Match[1])}</h1>`); continue; }

    const h2Match = trimmed.match(/^##\s+(.*)$/);
    if (h2Match) { output.push(`<h2 class="pnote-h2">${parseInlineMarkdown(h2Match[1])}</h2>`); continue; }

    const h3Match = trimmed.match(/^###\s+(.*)$/);
    if (h3Match) { output.push(`<h3 class="pnote-h3">${parseInlineMarkdown(h3Match[1])}</h3>`); continue; }

    const h4Match = trimmed.match(/^####\s+(.*)$/);
    if (h4Match) { output.push(`<h4 class="pnote-h4">${parseInlineMarkdown(h4Match[1])}</h4>`); continue; }

    // Code block placeholder
    if (/^@@@PNOTECODEBLOCK\d+@@@$/.test(trimmed)) { output.push(trimmed); continue; }

    // Math block placeholder
    if (/^@@@PNOTEMATHBLOCK\d+@@@$/.test(trimmed)) { output.push(trimmed); continue; }

    if (trimmed.length === 0) continue;

    // Regular paragraph
    output.push(`<p class="pnote-p">${parseInlineMarkdown(trimmed)}</p>`);
  }

  flushList();
  flushBlockquote();
  flushTable();

  let html = output.join('\n');

  // Replace math placeholders
  html = html.replace(/@@@PNOTEMATHBLOCK(\d+)@@@/g, (match, idx) => {
    const item = mathBlocks[Number(idx)];
    if (!item) return '';
    const formatted = formatMathFormula(item.formula);
    if (item.display) {
      return `<div class="pnote-math-display"><span class="pnote-math-tex">${formatted}</span></div>`;
    }
    return `<span class="pnote-math-inline"><span class="pnote-math-symbol">∑</span> ${formatted}</span>`;
  });

  // Replace code block placeholders
  html = html.replace(/@@@PNOTECODEBLOCK(\d+)@@@/g, (match, idx) => {
    const item = codeBlocks[Number(idx)];
    if (!item) return '';
    const rawCode = item.code.replace(/\n$/, '');
    const lang = item.lang || detectLanguageFromCode(rawCode);
    const langDisplay = getLanguageDisplayName(lang);
    const highlighted = SyntaxHighlighter.highlight(rawCode, lang);

    const linesArr = rawCode.split('\n');
    const lineCount = linesArr.length;

    const lineNumbersHtml = linesArr.map((_, i) => `<span>${i + 1}</span>`).join('');
    const blockId = 'pnoteCode_' + Math.random().toString(36).substring(2, 9);

    return `
      <div class="pnote-code-wrapper" id="${blockId}">
        <div class="pnote-code-header">
          <div class="pnote-code-meta">
            <span class="pnote-lang-badge pnote-lang-${lang.toLowerCase()}">${langDisplay}</span>
            <span class="pnote-line-count">${lineCount} line${lineCount === 1 ? '' : 's'}</span>
          </div>
          <button type="button" class="pnote-copy-code-btn" onclick="copyPnoteCodeBlock('${blockId}', this)" title="Copy source code to clipboard">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            <span>Copy Code</span>
          </button>
        </div>
        <div class="pnote-code-content-scroll">
          <div class="pnote-code-gutter" aria-hidden="true">${lineNumbersHtml}</div>
          <pre class="pnote-code-pre"><code class="pnote-code-inner language-${lang.toLowerCase()}">${highlighted}</code></pre>
        </div>
        <textarea class="pnote-raw-code-store" style="display:none;" aria-hidden="true">${escapeHtml(rawCode)}</textarea>
      </div>
    `;
  });

  return html;
}

function parseListBlock(rawLines) {
  let html = '';
  const stack = [];

  rawLines.forEach(line => {
    const ulMatch = line.match(/^(\s*)([-*+])\s+(.*)$/);
    const olMatch = line.match(/^(\s*)(\d+)\.\s+(.*)$/);
    const match = ulMatch || olMatch;
    if (!match) return;

    const indent = match[1].length;
    const type = ulMatch ? 'ul' : 'ol';
    const text = parseInlineMarkdown(match[3]);

    while (stack.length > 0 && stack[stack.length - 1].indent > indent) {
      const top = stack.pop();
      html += `</li></${top.type}>`;
    }

    if (stack.length === 0 || indent > stack[stack.length - 1].indent) {
      stack.push({ type, indent });
      html += `<${type} class="pnote-list${indent > 0 ? ' pnote-sublist' : ''}"><li>${text}`;
    } else if (stack[stack.length - 1].type !== type) {
      const top = stack.pop();
      html += `</li></${top.type}><${type} class="pnote-list"><li>${text}`;
      stack.push({ type, indent });
    } else {
      html += `</li><li>${text}`;
    }
  });

  while (stack.length > 0) {
    const top = stack.pop();
    html += `</li></${top.type}>`;
  }
  return html;
}

function parseInlineMarkdown(text) {
  if (!text) return '';
  let res = text;
  res = res.replace(/`([^`\n]+)`/g, (match, code) => `<code class="pnote-inline-code">${escapeHtml(code)}</code>`);
  res = res.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>');
  res = res.replace(/\*\*([^*]+)\*\*/g, '<strong class="pnote-bold">$1</strong>');
  res = res.replace(/__([^_]+)__/g, '<strong class="pnote-bold">$1</strong>');
  res = res.replace(/\*([^*]+)\*/g, '<em class="pnote-italic">$1</em>');
  res = res.replace(/_([^_]+)_/g, '<em class="pnote-italic">$1</em>');
  res = res.replace(/~~([^~]+)~~/g, '<del>$1</del>');
  res = res.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, url) => {
    const cleanUrl = escapeHtml(url.trim());
    return `<a href="${cleanUrl}" target="_blank" rel="noopener noreferrer" class="pnote-link">${label} ↗</a>`;
  });
  return res;
}

function formatMathFormula(tex) {
  let s = escapeHtml(tex.trim());
  s = s.replace(/\\mathcal\{O\}|\\mathcal\s+O/g, 'O');
  s = s.replace(/\\log/g, 'log');
  s = s.replace(/\\le\b/g, '≤');
  s = s.replace(/\\ge\b/g, '≥');
  s = s.replace(/\\ne\b/g, '≠');
  s = s.replace(/\\times\b/g, '×');
  s = s.replace(/\\to\b/g, '→');
  s = s.replace(/\\cdot\b/g, '·');
  s = s.replace(/\\sum/g, '∑');
  s = s.replace(/\\in\b/g, '∈');
  s = s.replace(/_\{([^}]+)\}/g, '<sub>$1</sub>');
  s = s.replace(/\^\{([^}]+)\}/g, '<sup>$1</sup>');
  s = s.replace(/\^2\b/g, '<sup>2</sup>');
  s = s.replace(/\^3\b/g, '<sup>3</sup>');
  s = s.replace(/\^k\b/g, '<sup>k</sup>');
  s = s.replace(/\^n\b/g, '<sup>n</sup>');
  s = s.replace(/_i\b/g, '<sub>i</sub>');
  s = s.replace(/_j\b/g, '<sub>j</sub>');
  return s;
}

function detectLanguageFromCode(code) {
  if (/^\s*(#include|class\s+\w+|std::|using\s+namespace|int\s+main|vector<)/m.test(code)) return 'cpp';
  if (/^\s*(def\s+\w+|import\s+\w+|from\s+\w+\s+import|class\s+\w+:)/m.test(code)) return 'python';
  if (/^\s*(public\s+class|public\s+static\s+void|package\s+\w+)/m.test(code)) return 'java';
  if (/^\s*(SELECT|INSERT\s+INTO|UPDATE|CREATE\s+TABLE|WITH\s+\w+\s+AS)/im.test(code)) return 'sql';
  if (/^\s*(function|const\s+\w+\s*=|let\s+\w+\s*=|import\s+.*from)/m.test(code)) return 'javascript';
  return 'cpp';
}

function getLanguageDisplayName(lang) {
  const l = (lang || '').toLowerCase().trim();
  const map = {
    'cpp': '⚙️ C++',
    'c++': '⚙️ C++',
    'c': '⚙️ C',
    'python': '🐍 Python',
    'py': '🐍 Python',
    'java': '☕ Java',
    'sql': '🗄️ SQL',
    'javascript': '🟨 JavaScript',
    'js': '🟨 JavaScript',
    'typescript': '🟦 TypeScript',
    'ts': '🟦 TypeScript',
    'bash': '🐚 Bash',
    'sh': '🐚 Shell',
    'text': '📄 Plain Text'
  };
  return map[l] || (lang ? lang.toUpperCase() : 'Code');
}

// 3. COPY CODE BLOCK HANDLER
function copyPnoteCodeBlock(blockId, btn) {
  const wrapper = document.getElementById(blockId);
  if (!wrapper) return;
  const store = wrapper.querySelector('.pnote-raw-code-store');
  const code = store ? store.value : (wrapper.querySelector('code')?.textContent || '');
  if (!code) return;

  const originalHtml = btn.innerHTML;
  const showFeedback = () => {
    btn.innerHTML = '<span style="color:#10b981; font-weight:700;">✓ Copied!</span>';
    setTimeout(() => { btn.innerHTML = originalHtml; }, 1800);
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(code).then(showFeedback).catch(() => fallbackCopyPnote(code, showFeedback));
  } else {
    fallbackCopyPnote(code, showFeedback);
  }
}

function fallbackCopyPnote(text, callback) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  try {
    document.execCommand('copy');
    if (callback) callback();
  } catch(e) {
    prompt('Copy code:', text);
  }
  document.body.removeChild(ta);
}

function copyProblemNotesToClipboard() {
  const ta = document.getElementById('pnoteEditTextarea');
  const text = ta && ta.value ? ta.value : (document.getElementById('probNoteContent')?.value || '');
  if (!text.trim()) {
    if (typeof showToast === 'function') showToast('No notes to copy');
    return;
  }
  const btn = document.getElementById('btnPnoteCopyAll');
  const originalHtml = btn ? btn.innerHTML : '';
  const showFeedback = () => {
    if (btn) {
      btn.innerHTML = '<span style="color:#10b981; font-weight:700;">✓ Copied All!</span>';
      setTimeout(() => { btn.innerHTML = originalHtml; }, 1800);
    }
    if (typeof showToast === 'function') showToast('Complete Markdown notes copied to clipboard 📋');
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(showFeedback).catch(() => fallbackCopyPnote(text, showFeedback));
  } else {
    fallbackCopyPnote(text, showFeedback);
  }
}

function editNotesFromViewer() {
  setPnoteMode('edit');
}

// 4. OPEN & VIEW PROBLEM NOTES MODAL CONTROLLER
function openViewProblemNotesModal() {
  const contentEl = document.getElementById('probNoteContent');
  const text = contentEl ? contentEl.value : '';
  pnoteOriginalText = text;

  const numEl = document.getElementById('revModalProbNum')?.textContent || '';
  const titleEl = document.getElementById('revModalProbTitle')?.textContent || '';

  const trackerPill = document.getElementById('viewNotesTrackerBadge');
  const probNumEl = document.getElementById('viewNotesProbNum');
  const diffBadge = document.getElementById('viewNotesProbDiff');
  const probTitleEl = document.getElementById('viewNotesProbTitle');
  const editorTa = document.getElementById('pnoteEditTextarea');

  const trackerTag = activeModalTracker === 'risingbrain' ? '🚀 RisingBrain' : activeModalTracker === 'striver' ? '📗 Striver A2Z' : '⚡ DSA Patterns';
  if (trackerPill) trackerPill.textContent = trackerTag;
  if (probNumEl) probNumEl.textContent = `Problem #${activeModalProbNum || 1}`;

  // Find difficulty
  let diff = 'Medium';
  let diffClass = 'diff-medium';
  if (numEl.toLowerCase().includes('easy')) { diff = 'Easy'; diffClass = 'diff-easy'; }
  else if (numEl.toLowerCase().includes('hard')) { diff = 'Hard'; diffClass = 'diff-hard'; }
  if (diffBadge) {
    diffBadge.textContent = diff;
    diffBadge.className = `pnote-diff-badge ${diffClass}`;
  }

  const cleanTitle = titleEl.replace(/^\[(RisingBrain|Striver A2Z|DSA Patterns)\]\s*/, '');
  if (probTitleEl) probTitleEl.textContent = cleanTitle || 'Problem Notes';

  if (editorTa) {
    editorTa.value = text;
  }

  isPnoteDirty = false;
  updatePnoteDirtyState(false);
  updatePnoteStats(text);

  // Render reading view
  renderPnoteReadingView(text);

  // Default to reading mode
  setPnoteMode('read');

  openModal('modalViewProblemNotes');
}

function renderPnoteReadingView(text) {
  const display = document.getElementById('viewNotesContentDisplay');
  if (!display) return;

  display.innerHTML = renderMarkdownToHtml(text);

  // Generate Table of Contents outline pills if headings exist
  generatePnoteTocOutline(display);
}

function generatePnoteTocOutline(container) {
  const tocBar = document.getElementById('pnoteTocBar');
  if (!tocBar) return;

  const headings = container.querySelectorAll('.pnote-h2, .pnote-h3');
  if (headings.length < 2) {
    tocBar.style.display = 'none';
    tocBar.innerHTML = '';
    return;
  }

  tocBar.style.display = 'flex';
  tocBar.innerHTML = '<span style="font-size:11px; font-weight:700; color:var(--text-dim); text-transform:uppercase; margin-right:0.25rem;">Sections:</span>' +
    Array.from(headings).map((h, idx) => {
      const text = h.textContent.replace(/^▸\s*/, '').trim();
      const hId = 'pnoteH_' + idx;
      h.id = hId;
      return `<button type="button" class="pnote-toc-pill" onclick="document.getElementById('${hId}')?.scrollIntoView({ behavior:'smooth', block:'start' })">${escapeHtml(text)}</button>`;
    }).join('');
}

// Mode toggle: 'read' | 'edit'
function setPnoteMode(mode) {
  pnoteCurrentMode = mode;
  const readBtn = document.getElementById('btnPnoteModeRead');
  const editBtn = document.getElementById('btnPnoteModeEdit');
  const readView = document.getElementById('pnoteReadingView');
  const editView = document.getElementById('pnoteEditingView');
  const readButtons = document.getElementById('pnoteReadButtons');
  const editButtons = document.getElementById('pnoteEditButtons');

  if (mode === 'read') {
    readBtn?.classList.add('active');
    editBtn?.classList.remove('active');
    if (readView) readView.style.display = 'flex';
    if (editView) editView.style.display = 'none';
    if (readButtons) readButtons.style.display = 'block';
    if (editButtons) editButtons.style.display = 'none';

    // Refresh reading view from textarea if edited
    const ta = document.getElementById('pnoteEditTextarea');
    if (ta) renderPnoteReadingView(ta.value);
  } else {
    readBtn?.classList.remove('active');
    editBtn?.classList.add('active');
    if (readView) readView.style.display = 'none';
    if (editView) editView.style.display = 'flex';
    if (readButtons) readButtons.style.display = 'none';
    if (editButtons) editButtons.style.display = 'flex';

    // Trigger live preview render
    updatePnoteLivePreview();
  }
}

// Sub-tab layout for editor: 'split' | 'write' | 'preview'
function setPnoteEditorLayout(layout) {
  pnoteEditorLayout = layout;
  const ws = document.getElementById('pnoteEditorWorkspace');
  if (ws) {
    ws.className = `pnote-editor-workspace layout-${layout}`;
  }
  document.querySelectorAll('.pnote-subtab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.id === 'btnPnoteSub' + layout.charAt(0).toUpperCase() + layout.slice(1));
  });
}

function handlePnoteEditorInput(val) {
  isPnoteDirty = (val !== pnoteOriginalText);
  updatePnoteDirtyState(isPnoteDirty);
  updatePnoteStats(val);

  clearTimeout(pnoteLivePreviewDebounce);
  pnoteLivePreviewDebounce = setTimeout(() => {
    updatePnoteLivePreview();
  }, 120);
}

function updatePnoteLivePreview() {
  const preview = document.getElementById('pnoteLivePreviewContent');
  const ta = document.getElementById('pnoteEditTextarea');
  if (preview && ta) {
    preview.innerHTML = renderMarkdownToHtml(ta.value);
  }
}

function updatePnoteStats(text) {
  const metaEl = document.getElementById('pnoteMetaStats');
  if (!metaEl) return;
  const len = text ? text.length : 0;
  const lines = text ? text.split('\n').length : 0;
  const words = text ? text.trim().split(/\s+/).filter(Boolean).length : 0;
  metaEl.textContent = `${len.toLocaleString()} characters · ${lines.toLocaleString()} lines · ${words.toLocaleString()} words`;
}

function updatePnoteDirtyState(dirty) {
  const dirtyBadge = document.getElementById('pnoteDirtyIndicator');
  if (dirtyBadge) dirtyBadge.style.display = dirty ? 'inline-flex' : 'none';
}

function handlePnoteEditorKeydown(e) {
  if (e.key === 'Tab') {
    e.preventDefault();
    const ta = e.target;
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    if (e.shiftKey) {
      const before = ta.value.substring(0, start);
      const lastLineIdx = before.lastIndexOf('\n') + 1;
      const lineStart = ta.value.substring(lastLineIdx, start);
      if (lineStart.startsWith('    ')) {
        ta.value = ta.value.substring(0, lastLineIdx) + ta.value.substring(lastLineIdx + 4);
        ta.selectionStart = ta.selectionEnd = Math.max(lastLineIdx, start - 4);
      }
    } else {
      ta.value = ta.value.substring(0, start) + '    ' + ta.value.substring(end);
      ta.selectionStart = ta.selectionEnd = start + 4;
    }
    handlePnoteEditorInput(ta.value);
  }
}

// Markdown Quick Insertion Helpers
function insertPnoteFmt(prefix, suffix = '') {
  const ta = document.getElementById('pnoteEditTextarea');
  if (!ta) return;
  const start = ta.selectionStart;
  const end = ta.selectionEnd;
  const selected = ta.value.substring(start, end);
  const replacement = prefix + selected + suffix;
  ta.value = ta.value.substring(0, start) + replacement + ta.value.substring(end);
  ta.focus();
  ta.selectionStart = start + prefix.length;
  ta.selectionEnd = start + prefix.length + selected.length;
  handlePnoteEditorInput(ta.value);
}

function insertPnoteCodeBlock(lang = 'cpp') {
  const snippet = `\n\`\`\`${lang}\n// C++ Solution Code\nclass Solution {\npublic:\n    \n};\n\`\`\`\n`;
  insertPnoteFmt(snippet, '');
}

function insertPnoteTable() {
  const tableSnippet = `\n| Approach | Time Complexity | Space Complexity | Status |\n| :--- | :---: | :---: | :--- |\n| Brute Force | O(N^2) | O(1) | TLE |\n| Optimal | O(N) | O(1) | Accepted |\n`;
  insertPnoteFmt(tableSnippet, '');
}

// Fullscreen toggle
function togglePnoteFullscreen() {
  const card = document.getElementById('pnoteModalCard');
  const label = document.getElementById('pnoteFullscreenLabel');
  if (!card) return;
  card.classList.toggle('fullscreen');
  const isFull = card.classList.contains('fullscreen');
  if (label) label.textContent = isFull ? 'Compress' : 'Full Screen';
}

// Save notes explicitly from viewer modal
function savePnoteExplicitlyFromModal() {
  const ta = document.getElementById('pnoteEditTextarea');
  const text = ta ? ta.value : '';

  // Sync to probNoteContent textarea in modalRevision
  const contentEl = document.getElementById('probNoteContent');
  if (contentEl) {
    contentEl.value = text;
    updateProbNotesCharCount(text);
  }

  saveProblemNotesExplicitly();

  pnoteOriginalText = text;
  isPnoteDirty = false;
  updatePnoteDirtyState(false);

  const saveBadge = document.getElementById('pnoteSavedIndicator');
  if (saveBadge) {
    saveBadge.style.display = 'inline-flex';
    setTimeout(() => { if (saveBadge) saveBadge.style.display = 'none'; }, 2000);
  }

  // Update reading mode article
  renderPnoteReadingView(text);

  // Switch to reading mode
  setPnoteMode('read');

  if (typeof showToast === 'function') {
    showToast('Problem notes saved successfully ✓');
  }
}

function cancelPnoteEdits() {
  if (isPnoteDirty) {
    const discard = confirm('You have unsaved changes in your notes. Discard changes and return to reading mode?');
    if (!discard) return;
  }
  const ta = document.getElementById('pnoteEditTextarea');
  if (ta) ta.value = pnoteOriginalText;
  isPnoteDirty = false;
  updatePnoteDirtyState(false);
  setPnoteMode('read');
}

function requestClosePnoteModal() {
  if (isPnoteDirty) {
    const shouldSave = confirm('You have unsaved changes in your problem notes.\n\nClick OK to SAVE before closing, or CANCEL to discard changes.');
    if (shouldSave) {
      savePnoteExplicitlyFromModal();
      closeModal('modalViewProblemNotes');
      return;
    }
  }
  closeModal('modalViewProblemNotes');
}

// Inline modalRevision notes tabs
function switchRevNotesTab(tab) {
  const editBtn = document.getElementById('btnRevTabEdit');
  const prevBtn = document.getElementById('btnRevTabPreview');
  const editWrap = document.getElementById('revNotesEditGroup');
  const prevWrap = document.getElementById('revNotesPreviewGroup');
  const prevContent = document.getElementById('revNotesPreviewContent');
  const contentEl = document.getElementById('probNoteContent');

  if (tab === 'edit') {
    editBtn?.classList.add('active');
    prevBtn?.classList.remove('active');
    if (editWrap) editWrap.style.display = 'block';
    if (prevWrap) prevWrap.style.display = 'none';
  } else {
    editBtn?.classList.remove('active');
    prevBtn?.classList.add('active');
    if (editWrap) editWrap.style.display = 'none';
    if (prevWrap) prevWrap.style.display = 'block';
    if (prevContent && contentEl) {
      prevContent.innerHTML = renderMarkdownToHtml(contentEl.value);
    }
  }
}
