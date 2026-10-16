const CONFIRM_MS = 48 * 60 * 60 * 1000;

export function classify(fields) {
  const trap = String(fields.company_website || "").trim();
  if (trap) return "honeypot";
  const email = String(fields.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return "bad_email";
  return "accept";
}

export async function sign(secret, email, exp) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const mac = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(`${email}|${exp}`),
  );
  return [...new Uint8Array(mac)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export function sameHex(left, right) {
  if (left.length !== right.length) return false;
  let diff = 0;
  for (let i = 0; i < left.length; i += 1) diff |= left.charCodeAt(i) ^ right.charCodeAt(i);
  return diff === 0;
}

function page(title, message) {
  const body = `<!doctype html><html lang="en"><meta charset="utf-8"><title>${title}</title><body><main><h1>${title}</h1><p>${message}</p><p><a href="https://aitoolsessentials.com/newsletter/">Keep/Cut Weekly</a></p></main></body></html>`;
  return new Response(body, { headers: { "content-type": "text/html; charset=utf-8" } });
}

async function resend(env, path, method, payload) {
  const response = await fetch(`https://api.resend.com${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: payload === undefined ? undefined : JSON.stringify(payload),
  });
  const text = await response.text();
  let data = {};
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { message: text };
    }
  }
  return { ok: response.ok, status: response.status, data };
}

async function limited(request) {
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  const origin = new URL(request.url).origin;
  const cache = caches.default;
  const key = new Request(`${origin}/rl/${encodeURIComponent(ip)}`);
  if (await cache.match(key)) return true;
  await cache.put(key, new Response("1", { headers: { "Cache-Control": "max-age=60" } }));
  return false;
}

async function startSignup(request, env) {
  if (!env.RESEND_API_KEY || !env.RESEND_SEGMENT_ID || !env.CONFIRM_SECRET) {
    return page("Signup is not ready", "The list is not accepting addresses yet.");
  }
  const form = await request.formData();
  const fields = {
    email: form.get("email"),
    company_website: form.get("company_website"),
  };
  const kind = classify(fields);
  if (kind === "honeypot") return page("Check your email", "If that address can join, a confirm link is on its way.");
  if (kind === "bad_email") return page("Check the address", "Enter a full email address.");
  if (await limited(request)) return page("Slow down", "Wait a minute, then try the form again.");

  const email = String(fields.email).trim().toLowerCase();
  const encoded = encodeURIComponent(email);
  const existing = await resend(env, `/contacts/${encoded}`, "GET");
  if (existing.ok && existing.data.unsubscribed === false) {
    return page("Already confirmed", "That address is already on Keep/Cut Weekly.");
  }
  if (!existing.ok) {
    const created = await resend(env, "/contacts", "POST", { email, unsubscribed: true });
    if (!created.ok && created.status !== 409) {
      return page("Try again", "The list did not save that address.");
    }
  }
  const segment = encodeURIComponent(env.RESEND_SEGMENT_ID);
  await resend(env, `/contacts/${encoded}/segments/${segment}`, "POST");

  const exp = Date.now() + CONFIRM_MS;
  const token = await sign(env.CONFIRM_SECRET, email, exp);
  const link = `${new URL(request.url).origin}/confirm?email=${encoded}&exp=${exp}&token=${token}`;
  const mailed = await resend(env, "/emails", "POST", {
    from: env.FROM_ADDRESS,
    to: [email],
    subject: "Confirm Keep/Cut Weekly",
    html: `<p>Confirm Keep/Cut Weekly. Nothing is added until you open this link.</p><p><a href="${link}">Confirm this address</a></p><p>AIToolsEssentials, 1090 West Foothill, Claremont, CA 91711.</p>`,
  });
  if (!mailed.ok) return page("Try again", "The confirm message did not send.");
  return page("Check your email", "Open the confirm link. The list stays empty until you do.");
}

async function confirm(url, env) {
  if (!env.RESEND_API_KEY || !env.CONFIRM_SECRET) {
    return page("Signup is not ready", "The list is not accepting addresses yet.");
  }
  const email = String(url.searchParams.get("email") || "").trim().toLowerCase();
  const exp = String(url.searchParams.get("exp") || "");
  const token = String(url.searchParams.get("token") || "");
  if (classify({ email }) !== "accept" || !/^\d+$/.test(exp)) {
    return page("Link expired", "Request a new confirm link from the subscribe page.");
  }
  if (Number(exp) < Date.now()) {
    return page("Link expired", "Request a new confirm link from the subscribe page.");
  }
  const expected = await sign(env.CONFIRM_SECRET, email, exp);
  if (!sameHex(expected, token)) {
    return page("Link expired", "Request a new confirm link from the subscribe page.");
  }
  const updated = await resend(env, `/contacts/${encodeURIComponent(email)}`, "PATCH", {
    unsubscribed: false,
  });
  if (!updated.ok) return page("Try again", "That confirm link did not finish.");
  return page("You are confirmed", "Keep/Cut Weekly will include this address from the next approved issue.");
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "POST" && (url.pathname === "/" || url.pathname === "")) {
      return startSignup(request, env);
    }
    if (request.method === "GET" && url.pathname === "/confirm") return confirm(url, env);
    return page("Keep/Cut Weekly", "Use the subscribe form on AIToolsEssentials.");
  },
};
