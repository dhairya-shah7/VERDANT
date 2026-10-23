import urllib.request
import urllib.parse
import json
import re
import sympy

NUMBER_WORDS = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
    'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
    'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
    'eighty': 80, 'ninety': 90, 'hundred': 100, 'thousand': 1000
}

OPERATORS = {
    'plus': '+', 'add': '+', 'added to': '+',
    'minus': '-', 'subtract': '-', 'less': '-',
    'times': '*', 'multiply': '*', 'multiplied by': '*',
    'divided by': '/', 'over': '/', 'divide': '/',
    'squared': '**2', 'cubed': '**3'
}

def solve_math(query: str):
    q = query.lower().strip()
    q = re.sub(r'^(what is|calculate|compute|solve|how much is)\s+', '', q)
    q = q.rstrip(' ?.!\"\'')

    # Replace operator phrases
    for op_word, op_sym in sorted(OPERATORS.items(), key=lambda x: -len(x[0])):
        q = re.sub(r'\b' + re.escape(op_word) + r'\b', f' {op_sym} ', q)

    # Replace word numbers with digits
    tokens = q.split()
    converted = []
    for tok in tokens:
        if tok in NUMBER_WORDS:
            converted.append(str(NUMBER_WORDS[tok]))
        else:
            converted.append(tok)

    expr = ' '.join(converted)
    # Sanitize: allow only digits, operators, parens, dots, spaces, sympy functions
    if re.match(r'^[\d\s\+\-\*\/\.\(\)\^]+$', expr):
        try:
            val = sympy.sympify(expr)
            if hasattr(val, 'is_integer') and val.is_integer:
                val = int(val)
            original_clean = query.strip(' ?.!\"\'')
            speech = f"{original_clean} equals {val}."
            return True, {
                "kind": "MATH_CALCULATION",
                "title": f"Calculation: {expr} = {val}",
                "speech_output": speech,
                "display_data": {
                    "expression": expr,
                    "result": str(val),
                    "speech": speech,
                    "engine": "SymbolicMathEngine"
                }
            }
        except Exception:
            pass
    return False, None

def search_wikipedia(query: str):
    clean_q = re.sub(r'^(who (is|was)( the| a)?|what (is|are)( the| a)?|tell me about|explain)\s+', '', query, flags=re.I)
    clean_q = clean_q.rstrip(' ?.!\"\'')
    
    # Check for "builder of X" or "founder of X"
    target = clean_q
    builder_match = re.search(r'(?:builder|founder|creator) of\s+(.+)', clean_q, flags=re.I)
    if builder_match:
        target = builder_match.group(1).strip()

    encoded = urllib.parse.quote(target)
    headers = {'User-Agent': 'AlexaAthenaSentinel/2.0 (hackathon@amazon.com)'}
    
    # 1. Opensearch
    search_url = f'https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded}&limit=3&namespace=0&format=json'
    req = urllib.request.Request(search_url, headers=headers)
    with urllib.request.urlopen(req, timeout=4) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        titles = data[1] if len(data) > 1 else []
        
    if not titles:
        titles = [target]
        
    target_title = titles[0]
    sum_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(target_title)}'
    req2 = urllib.request.Request(sum_url, headers=headers)
    with urllib.request.urlopen(req2, timeout=4) as resp2:
        d2 = json.loads(resp2.read().decode('utf-8'))
        extract = d2.get('extract', '')
        title = d2.get('title', target_title)
        
        # Split extract into clean sentences (first 2-3 sentences)
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', extract) if s.strip()]
        selected = ' '.join(sentences[:3]) if sentences else extract
        
        return True, {
            "kind": "DETAILED_KNOWLEDGE",
            "title": title,
            "speech_output": selected,
            "display_data": {
                "title": title,
                "extract": selected,
                "source": f"Global Verified Knowledge: {title}",
                "depth": "3-4 Sentence Salience Synthesis"
            }
        }

if __name__ == '__main__':
    for test in ['What is one plus one', 'What is 15 times 4', 'Who is the Builder of open AI', 'Who is Elon Musk']:
        is_math, res = solve_math(test)
        if is_math:
            print(f"MATH: {test} -> {res['speech_output']}")
        else:
            success, res = search_wikipedia(test)
            print(f"KNOWLEDGE: {test} -> {res['title']} | {res['speech_output'][:100]}...")
