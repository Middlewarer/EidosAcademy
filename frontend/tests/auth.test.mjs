import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const source = (await readFile(new URL('../src/components/api/apiRequest.jsx', import.meta.url), 'utf8')).replace('import.meta.env.VITE_API_URL', '"http://api.test"');
let iteration = 0;
async function setup() {
    let queue = Promise.resolve();
    Object.defineProperty(globalThis, 'navigator', { configurable: true, value: {
        locks: { request: (_name, action) => {
            const result = queue.then(action);
            queue = result.catch(() => {});
            return result;
        } },
    } });
    const store = new Map();
    globalThis.localStorage = { getItem: k => store.get(k) ?? null, setItem: (k,v) => store.set(k,String(v)), removeItem: k => store.delete(k) };
    globalThis.window = new EventTarget();
    const api = await import(`data:text/javascript;base64,${Buffer.from(source + '\n//' + iteration++).toString('base64')}`);
    api.saveTokens('old', 'refresh-old');
    return api;
}
const reply = (status, data = {}) => new Response(JSON.stringify(data), { status });

test('parallel 401s share refresh and preserve POST on retry', async () => {
    const api = await setup(); let refreshes = 0; let attempts = 0;
    globalThis.fetch = async (url, options) => {
        if (url.endsWith('/refresh/')) { refreshes++; await new Promise(resolve => setTimeout(resolve, 10)); return reply(200,{access:'new',refresh:'rotated'}); }
        assert.equal(options.method,'POST'); assert.equal(options.body,'{"topic":1}');
        attempts++; return reply(options.headers.get('Authorization') === 'Bearer new' ? 200 : 401);
    };
    const results = await Promise.all([api.apiRequest('/api/complete/',{method:'POST',body:'{"topic":1}'}),api.apiRequest('/api/complete/',{method:'POST',body:'{"topic":1}'})]);
    assert.ok(results.every(r => r.ok)); assert.equal(refreshes,1); assert.equal(attempts,4);
    assert.equal(localStorage.getItem('refresh_token'),'rotated');
});
test('public login 401 does not refresh or erase session', async () => {
    const api=await setup(); let calls=0;
    globalThis.fetch=async (_url,options)=> { calls++; assert.equal(options.headers.has('Authorization'),false); return reply(401); };
    assert.equal((await api.apiRequest('/api/token/',{method:'POST'})).status,401);
    assert.equal(calls,1); assert.equal(localStorage.getItem('access_token'),'old');
});
test('invalid refresh clears session and notifies context', async () => {
    const api=await setup(); let events=0; window.addEventListener('auth:expired',()=>events++);
    globalThis.fetch=async ()=>reply(401);
    await api.apiRequest('/api/me/'); assert.equal(events,1); assert.equal(localStorage.getItem('access_token'),null);
});
test('server failure preserves tokens', async () => {
    const api=await setup(); globalThis.fetch=async url=>reply(url.endsWith('/refresh/')?503:401);
    await assert.rejects(api.apiRequest('/api/me/')); assert.equal(localStorage.getItem('refresh_token'),'refresh-old');
});
test('failed retry stops and clears session', async () => {
    const api=await setup(); let calls=0;
    globalThis.fetch=async url=> { calls++;return url.endsWith('/refresh/')?reply(200,{access:'new'}):reply(401); };
    assert.equal((await api.apiRequest('/api/me/')).status,401); assert.equal(calls,3);assert.equal(localStorage.getItem('access_token'),null);
});
test('logout during refresh cannot resurrect session', async () => {
    const api=await setup(); let finish; let started;
    const ready=new Promise(r=>started=r);
    globalThis.fetch=async url=> { if(url.endsWith('/refresh/')) { started(); return new Promise(r=>finish=r); } return reply(401); };
    const pending=api.apiRequest('/api/me/');await ready;api.clearSession();finish(reply(200,{access:'new',refresh:'new'}));await pending;
    assert.equal(localStorage.getItem('access_token'),null);
});
test('logout revokes rotated token before clearing', async () => {
    const api=await setup(); let revoked;
    globalThis.fetch=async (_url,options)=> { revoked=JSON.parse(options.body).refresh;return reply(200); };
    await api.logoutSession();assert.equal(revoked,'refresh-old');assert.equal(localStorage.getItem('refresh_token'),null);
});


test('two tabs rotate once and keep the shared session', async () => {
    const first = await setup();
    const second = await import(`data:text/javascript;base64,${Buffer.from(source + '\n//tab' + iteration++).toString('base64')}`);
    let refreshes = 0;
    globalThis.fetch = async (url, options) => {
        if (url.endsWith('/refresh/')) {
            refreshes++;
            await new Promise(resolve => setTimeout(resolve, 10));
            return refreshes === 1 ? reply(200, {access:'new',refresh:'rotated'}) : reply(401);
        }
        return reply(options.headers.get('Authorization') === 'Bearer new' ? 200 : 401);
    };
    const session = first.getSessionId();
    const responses = await Promise.all([first.apiRequest('/api/me/'),second.apiRequest('/api/me/')]);
    assert.deepEqual(responses.map(r=>r.status),[200,200]);
    assert.equal(refreshes,1);
    assert.equal(localStorage.getItem('refresh_token'),'rotated');
    assert.equal(first.getSessionId(),session);
});

test('old failed refresh cannot clear a newly signed-in account', async () => {
    const first = await setup();
    const second = await import(`data:text/javascript;base64,${Buffer.from(source + '\n//tab' + iteration++).toString('base64')}`);
    let finish, started;
    const ready = new Promise(resolve=>started=resolve);
    globalThis.fetch = async url => {
        if (url.endsWith('/refresh/')) { started(); return new Promise(resolve=>finish=resolve); }
        return reply(401);
    };
    const request = first.apiRequest('/api/me/');
    await ready;
    second.saveTokens('account-b','refresh-b');
    finish(reply(401));
    await request;
    assert.equal(localStorage.getItem('access_token'),'account-b');
    assert.equal(localStorage.getItem('refresh_token'),'refresh-b');
});

test('logout in second tab waits for rotation and revokes latest refresh', async () => {
    const first = await setup();
    const second = await import(`data:text/javascript;base64,${Buffer.from(source + '\n//tab' + iteration++).toString('base64')}`);
    let finish, started, revoked;
    const ready=new Promise(resolve=>started=resolve);
    globalThis.fetch=async (url,options)=> {
        if(url.endsWith('/refresh/')) { started();return new Promise(resolve=>finish=resolve); }
        if(url.endsWith('/logout/')) { revoked=JSON.parse(options.body).refresh;return reply(200); }
        return reply(options.headers.get('Authorization')==='Bearer new'?200:401);
    };
    const pending=first.apiRequest('/api/me/'); await ready;
    const logout=second.logoutSession();
    finish(reply(200,{access:'new',refresh:'rotated'}));
    await Promise.all([pending,logout]);
    assert.equal(revoked,'rotated');
    assert.equal(localStorage.getItem('access_token'),null);
});
