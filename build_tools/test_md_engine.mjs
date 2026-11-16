// Comprehensive standalone markdown & syntax highlighting engine test

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// 1. SYNTAX HIGHLIGHTING ENGINE
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
    // Default heuristic: if code has typical C++ patterns, highlight as C++
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

      if (comment) {
        result += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
      } else if (string) {
        result += `<span class="tok-string">${escapeHtml(string)}</span>`;
      } else if (macro) {
        result += `<span class="tok-macro">${escapeHtml(macro)}</span>`;
      } else if (number) {
        result += `<span class="tok-num">${escapeHtml(number)}</span>`;
      } else if (keyword) {
        result += `<span class="tok-kw">${escapeHtml(keyword)}</span>`;
      } else if (type) {
        result += `<span class="tok-type">${escapeHtml(type)}</span>`;
      } else if (op) {
        result += `<span class="tok-op">${escapeHtml(op)}</span>`;
      } else {
        result += escapeHtml(full);
      }

      lastIndex = tokenRegex.lastIndex;
    }

    if (lastIndex < code.length) {
      result += escapeHtml(code.slice(lastIndex));
    }

    return result;
  },

  highlightPython(code) {
    const tokenRegex = /(#[^\r\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b\d+(?:\.\d+)?\b)|(\b(?:def|class|return|if|elif|else|for|while|break|continue|in|not|and|or|is|import|from|as|try|except|finally|raise|with|yield|lambda|pass|global|nonlocal|async|await)\b)|(\b(?:self|None|True|False|print|len|range|enumerate|zip|map|filter|int|float|str|list|dict|set|tuple|bool|min|max|sum|sorted|open|isinstance)\b)|(<=|>=|==|!=|\+=|-=|\*=|\/=|->|[+\-*/%=&|^~<>]+)/g;

    let result = '';
    let lastIndex = 0;
    let match;

    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) {
        result += escapeHtml(code.slice(lastIndex, match.index));
      }
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

    let result = '';
    let lastIndex = 0;
    let match;

    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) {
        result += escapeHtml(code.slice(lastIndex, match.index));
      }
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

    let result = '';
    let lastIndex = 0;
    let match;

    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) {
        result += escapeHtml(code.slice(lastIndex, match.index));
      }
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

    let result = '';
    let lastIndex = 0;
    let match;

    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) {
        result += escapeHtml(code.slice(lastIndex, match.index));
      }
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

    let result = '';
    let lastIndex = 0;
    let match;

    while ((match = tokenRegex.exec(code)) !== null) {
      if (match.index > lastIndex) {
        result += escapeHtml(code.slice(lastIndex, match.index));
      }
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

// 2. MARKDOWN RENDERER
function renderMarkdownToHtml(rawMarkdown) {
  if (!rawMarkdown || !rawMarkdown.trim()) {
    return '<div class="pnote-empty-state">No notes written yet. Click <b>Edit Notes</b> to write or paste technical notes.</div>';
  }

  let text = rawMarkdown.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  // Placeholders
  const codeBlocks = [];
  const mathBlocks = [];

  // 1. Extract fenced code blocks
  text = text.replace(/```([a-zA-Z0-9_\-+]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    const id = codeBlocks.length;
    codeBlocks.push({ lang: lang.trim(), code: code });
    return `@@@PNOTE_CODE_BLOCK_${id}@@@`;
  });

  // 2. Extract display math ($$...$$)
  text = text.replace(/\$\$([\s\S]*?)\$\$/g, (match, formula) => {
    const id = mathBlocks.length;
    mathBlocks.push({ display: true, formula: formula.trim() });
    return `@@@PNOTE_MATH_BLOCK_${id}@@@`;
  });

  // 3. Extract inline math ($...$)
  text = text.replace(/(^|[^\\])\$([^\$\n]+?)\$/g, (match, prefix, formula) => {
    const id = mathBlocks.length;
    mathBlocks.push({ display: false, formula: formula.trim() });
    return `${prefix}@@@PNOTE_MATH_BLOCK_${id}@@@`;
  });

  // Split text into lines
  const lines = text.split('\n');
  const output = [];
  let inList = false;
  let listType = null;
  let listItems = [];
  let inBlockquote = false;
  let blockquoteLines = [];
  let inTable = false;
  let tableRows = [];

  const flushList = () => {
    if (!inList) return;
    const tag = listType;
    let listHtml = `<${tag} class="pnote-list">`;
    listItems.forEach(item => {
      // Check if item has sub-lines
      const parts = item.split('\n');
      const firstLine = parts[0];
      const rest = parts.slice(1).map(r => `<div class="pnote-list-sub">${parseInlineMarkdown(r)}</div>`).join('');
      listHtml += `<li>${parseInlineMarkdown(firstLine)}${rest}</li>`;
    });
    listHtml += `</${tag}>`;
    output.push(listHtml);
    inList = false;
    listType = null;
    listItems = [];
  };

  const flushBlockquote = () => {
    if (!inBlockquote) return;
    const fullText = blockquoteLines.join('\n');
    let calloutType = 'note';
    let calloutIcon = '💡';
    let calloutTitle = 'Note';
    let bodyText = fullText;

    const calloutMatch = fullText.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](?:\s*([^\n]*))?\n?([\s\S]*)$/i);
    if (calloutMatch) {
      const type = calloutMatch[1].toUpperCase();
      const customTitle = calloutMatch[2];
      bodyText = calloutMatch[3] || '';
      if (type === 'NOTE') {
        calloutType = 'note';
        calloutIcon = '📘';
        calloutTitle = customTitle || 'Note';
      } else if (type === 'TIP') {
        calloutType = 'tip';
        calloutIcon = '💡';
        calloutTitle = customTitle || 'Tip / Key Idea';
      } else if (type === 'IMPORTANT') {
        calloutType = 'important';
        calloutIcon = '⭐';
        calloutTitle = customTitle || 'Important';
      } else if (type === 'WARNING') {
        calloutType = 'warning';
        calloutIcon = '⚠️';
        calloutTitle = customTitle || 'Warning / Caution';
      } else if (type === 'CAUTION') {
        calloutType = 'danger';
        calloutIcon = '🚨';
        calloutTitle = customTitle || 'Edge Case';
      }
    } else if (/^\*\*(?:Key\s*Idea|Idea|Invariant|Intuition|Crux):\*\*/i.test(fullText)) {
      calloutType = 'tip';
      calloutIcon = '💡';
      calloutTitle = 'Key Invariant / Idea';
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
      tableRows.forEach(r => output.push(`<p>${parseInlineMarkdown(r)}</p>`));
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

    // 1. Check Table row
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      flushList();
      flushBlockquote();
      inTable = true;
      tableRows.push(trimmed);
      continue;
    } else if (inTable) {
      flushTable();
    }

    // 2. Check Blockquote
    if (trimmed.startsWith('>')) {
      flushList();
      inBlockquote = true;
      blockquoteLines.push(trimmed.replace(/^>\s?/, ''));
      continue;
    } else if (inBlockquote) {
      flushBlockquote();
    }

    // 3. Check Lists
    const ulMatch = line.match(/^(\s*)([-*+])\s+(.*)$/);
    const olMatch = line.match(/^(\s*)(\d+)\.\s+(.*)$/);

    if (ulMatch) {
      if (inList && listType !== 'ul') flushList();
      inList = true;
      listType = 'ul';
      listItems.push(ulMatch[3]);
      continue;
    } else if (olMatch) {
      if (inList && listType !== 'ol') flushList();
      inList = true;
      listType = 'ol';
      listItems.push(olMatch[3]);
      continue;
    } else if (inList) {
      if (/^\s{2,}/.test(line) && trimmed.length > 0) {
        if (listItems.length > 0) {
          listItems[listItems.length - 1] += '\n' + trimmed;
        }
        continue;
      } else {
        flushList();
      }
    }

    // 4. Horizontal Rule
    if (/^(\-{3,}|\*{3,}|_{3,})$/.test(trimmed)) {
      output.push('<hr class="pnote-hr">');
      continue;
    }

    // 5. Headings
    const h1Match = trimmed.match(/^#\s+(.*)$/);
    if (h1Match) {
      output.push(`<h1 class="pnote-h1">${parseInlineMarkdown(h1Match[1])}</h1>`);
      continue;
    }

    const h2Match = trimmed.match(/^##\s+(.*)$/);
    if (h2Match) {
      output.push(`<h2 class="pnote-h2">${parseInlineMarkdown(h2Match[1])}</h2>`);
      continue;
    }

    const h3Match = trimmed.match(/^###\s+(.*)$/);
    if (h3Match) {
      output.push(`<h3 class="pnote-h3">${parseInlineMarkdown(h3Match[1])}</h3>`);
      continue;
    }

    const h4Match = trimmed.match(/^####\s+(.*)$/);
    if (h4Match) {
      output.push(`<h4 class="pnote-h4">${parseInlineMarkdown(h4Match[1])}</h4>`);
      continue;
    }

    // 6. Code block placeholder alone on line
    if (/^@@@PNOTE_CODE_BLOCK_\d+@@@$/.test(trimmed)) {
      output.push(trimmed);
      continue;
    }

    // 7. Math block placeholder
    if (/^@@@PNOTE_MATH_BLOCK_\d+@@@$/.test(trimmed)) {
      output.push(trimmed);
      continue;
    }

    // 8. Empty lines
    if (trimmed.length === 0) {
      continue;
    }

    // 9. Regular Paragraph
    output.push(`<p class="pnote-p">${parseInlineMarkdown(trimmed)}</p>`);
  }

  flushList();
  flushBlockquote();
  flushTable();

  let html = output.join('\n');

  // Replace math placeholders
  html = html.replace(/@@@PNOTE_MATH_BLOCK_(\d+)@@@/g, (match, idx) => {
    const item = mathBlocks[Number(idx)];
    if (!item) return '';
    const formulaHtml = escapeHtml(item.formula);
    if (item.display) {
      return `<div class="pnote-math-display"><span class="pnote-math-tex">${formulaHtml}</span></div>`;
    }
    return `<span class="pnote-math-inline"><span class="pnote-math-symbol">∑</span> ${formulaHtml}</span>`;
  });

  // Replace code block placeholders
  html = html.replace(/@@@PNOTE_CODE_BLOCK_(\d+)@@@/g, (match, idx) => {
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
          <button type="button" class="pnote-copy-code-btn" onclick="copyPnoteCodeBlock('${blockId}', this)" title="Copy source code">
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

function parseInlineMarkdown(text) {
  if (!text) return '';
  let res = text;

  // 1. Inline code: `code`
  res = res.replace(/`([^`\n]+)`/g, (match, code) => {
    return `<code class="pnote-inline-code">${escapeHtml(code)}</code>`;
  });

  // 2. Bold & Italic: ***text***
  res = res.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>');

  // 3. Bold: **text** or __text__
  res = res.replace(/\*\*([^*]+)\*\*/g, '<strong class="pnote-bold">$1</strong>');
  res = res.replace(/__([^_]+)__/g, '<strong class="pnote-bold">$1</strong>');

  // 4. Italic: *text* or _text_
  res = res.replace(/\*([^*]+)\*/g, '<em class="pnote-italic">$1</em>');
  res = res.replace(/_([^_]+)_/g, '<em class="pnote-italic">$1</em>');

  // 5. Strikethrough: ~~text~~
  res = res.replace(/~~([^~]+)~~/g, '<del>$1</del>');

  // 6. Links: [text](url)
  res = res.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, url) => {
    const cleanUrl = escapeHtml(url.trim());
    return `<a href="${cleanUrl}" target="_blank" rel="noopener noreferrer" class="pnote-link">${label} ↗</a>`;
  });

  return res;
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

// Test with user sample!
const sampleNotes = `### Approach 1: Brute Force — O(N²)

**Idea:**

Generate all possible subarrays and maintain a running sum.

**Algorithm:**
1. Initialize \`count = 0\`.
2. Select the starting index.
3. Traverse the remaining elements.
   - Add \`nums[j]\` to sum.
   - If \`sum == k\`, increment \`count\`.

> [!NOTE]
> This approach takes $O(N^2)$ time and $O(1)$ space. Can we do better using a Hash Map?

### Approach 2: Prefix Sum + Hash Map — O(N) Optimal

**Key Invariant:**
If \`prefSum[j] - prefSum[i] = k\`, then \`prefSum[i] = prefSum[j] - k\`.

| Approach | Time Complexity | Space Complexity | Status |
| :--- | :---: | :---: | :--- |
| Brute Force | $O(N^2)$ | $O(1)$ | TLE on LeetCode |
| Prefix Sum Map | $O(N)$ | $O(N)$ | Accepted (Optimal) |

**C++ Code:**
\`\`\`cpp
#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> prefixCounts;
        prefixCounts[0] = 1; // Base case: prefix sum of 0 appears once
        
        int currentSum = 0;
        int count = 0;
        
        for (int num : nums) {
            currentSum += num;
            int target = currentSum - k;
            
            if (prefixCounts.find(target) != prefixCounts.end()) {
                count += prefixCounts[target];
            }
            prefixCounts[currentSum]++;
        }
        
        return count;
    }
};
\`\`\`
`;

const rendered = renderMarkdownToHtml(sampleNotes);
console.log("=== RENDERED HTML PREVIEW ===");
console.log(rendered.substring(0, 1000));
console.log("\n...\n");
console.log("Total rendered length:", rendered.length);
console.log("Contains code-wrapper?", rendered.includes("pnote-code-wrapper"));
console.log("Contains tok-kw for class?", rendered.includes('<span class="tok-kw">class</span>'));
console.log("Contains tok-type for vector?", rendered.includes('<span class="tok-type">vector</span>'));
console.log("Contains table?", rendered.includes('<table class="pnote-table">'));
console.log("Contains callout?", rendered.includes('pnote-callout-note'));
console.log("Contains h3?", rendered.includes('<h3 class="pnote-h3">Approach 1:'));
