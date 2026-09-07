import urllib.request
import json

base = 'http://127.0.0.1:5000/api/medsearch'

def post(path, data):
    req = urllib.request.Request(base + path, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

def get(path):
    return json.loads(urllib.request.urlopen(base + path, timeout=15).read())

print('=== T26: 会话初始化与关键词提取 ===')
session = post('/sessions', {})
session_id = session['data']['session_id']
print(f'1. Session created: {session_id}')

extract = post('/keywords/extract', {'description': '肺腺癌患者EGFR突变与预后的相关性研究'})
keywords = extract['data']['keywords']
print(f'2. Keywords extracted: {keywords}')

print('\n=== T27: 关键词管理与检索触发 ===')
translate = post('/keywords/translate', {'keywords': keywords})
print(f'3. Keywords translated: {translate["data"]["translations"]}')

search = post('/literature/search', {'session_id': session_id, 'keywords': keywords})
task_id = search['data']['task_id']
total = search['data']['total']
filtered = search['data']['filtered']
literatures = search['data']['literatures']
print(f'4. Search started: task_id={task_id}, total={total}, filtered={filtered}')
print(f'   First literature: {literatures[0]["title"][:50] if literatures else "none"}...')

print('\n=== T28: 文献列表分页与勾选 ===')
if literatures:
    pmid = literatures[0]['pmid']
    select = post('/literatures/select', {'session_id': session_id, 'pmid': pmid, 'selected': True})
    print(f'5. Selected PMID {pmid}: selected_count={select["data"]["selected_count"]}')

    if len(literatures) > 1:
        pmid2 = literatures[1]['pmid']
        select2 = post('/literatures/select', {'session_id': session_id, 'pmid': pmid2, 'selected': True})
        print(f'6. Selected PMID {pmid2}: selected_count={select2["data"]["selected_count"]}')

print('\n=== T29: AI总结生成与原文跳转 ===')
if literatures:
    selected_pmids = [lit['pmid'] for lit in literatures[:2]]
    summary = post('/summary/generate', {'session_id': session_id, 'pmids': selected_pmids})
    meta = summary['data']['meta']
    print(f'7. Summary generated:')
    print(f'   Title CN: {meta["title_cn"][:50]}...')
    print(f'   Authors: {meta["authors"][:30]}...')
    print(f'   PMID: {meta["pmid"]}')
    print(f'   Original URL: {meta["original_url"]}')
    print(f'   Key findings: {len(summary["data"]["key_findings"])} items')
    print(f'   Research trends: {len(summary["data"]["research_trends"])} items')
    print(f'   Clinical significance: {len(summary["data"]["clinical_significance"])} items')
    print(f'   Disclaimer: {summary["data"]["disclaimer"]}')

print('\n=== All end-to-end tests passed! ===')