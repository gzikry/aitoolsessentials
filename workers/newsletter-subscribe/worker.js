const CONFIRM_MS = 48 * 60 * 60 * 1000;
const WATCH_PROPERTY = "price_watch";
const WATCH_LIMIT = 20;

// Price-alert forms post a tool slug. Anything that is not a plain slug is dropped.
export function watchSlug(value) {
  const slug = String(value || "").trim().toLowerCase();
  return /^[a-z0-9][a-z0-9-]{0,63}$/.test(slug) ? slug : "";
}

// Comma list of watched slugs, newest last, capped so the property stays small.
export function mergeWatch(existing, slug) {
  const list = String(existing || "")
    .split(",")
    .map((item) => watchSlug(item))
    .filter(Boolean);
  if (slug && !list.includes(slug)) list.push(slug);
  return list.slice(-WATCH_LIMIT).join(",");
}

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
  const body = `<!doctype html><html lang="en"><meta charset="utf-8"><title>${title}</title><body><main><h1>${title}</h1><p>${message}</p><p><a href="https://aitoolsessentials.com/newsletter/">Keep, Test, Cut</a></p></main></body></html>`;
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

export async function limited(request, env) {
  const limiter = env && env.SIGNUP_LIMIT;
  if (!limiter || typeof limiter.limit !== "function") return true;
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  try {
    const { success } = await limiter.limit({ key: ip });
    return success !== true;
  } catch {
    return true;
  }
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
  const watch = watchSlug(form.get("tool"));
  const kind = classify(fields);
  if (kind === "honeypot") return page("Check your email", "If that address can join, a confirm link is on its way.");
  if (kind === "bad_email") return page("Check the address", "Enter a full email address.");
  if (await limited(request, env)) return page("Slow down", "Wait a minute, then try the form again.");

  const email = String(fields.email).trim().toLowerCase();
  const encoded = encodeURIComponent(email);
  const existing = await resend(env, `/contacts/${encoded}`, "GET");
  const known = existing.ok ? existing.data : {};
  if (existing.ok && known.unsubscribed === false) {
    if (watch) {
      await recordWatch(env, encoded, known, watch);
      return page("Price alert added", "That address is already confirmed. We added this tool to its price alerts.");
    }
    return page("Already confirmed", "That address is already on Keep, Test, Cut.");
  }
  if (!existing.ok) {
    const created = await resend(env, "/contacts", "POST", { email, unsubscribed: true });
    if (!created.ok && created.status !== 409) {
      return page("Try again", "The list did not save that address.");
    }
  }
  const segment = encodeURIComponent(env.RESEND_SEGMENT_ID);
  await resend(env, `/contacts/${encoded}/segments/${segment}`, "POST");
  if (watch) await recordWatch(env, encoded, known, watch);

  const exp = Date.now() + CONFIRM_MS;
  const token = await sign(env.CONFIRM_SECRET, email, exp);
  const link = `${new URL(request.url).origin}/confirm?email=${encoded}&exp=${exp}&token=${token}`;
  const mailed = await resend(env, "/emails", "POST", {
    from: env.FROM_ADDRESS,
    to: [email],
    subject: watch ? "Confirm your price alert" : "Confirm Keep, Test, Cut",
    html: `<p>${watch ? "Confirm your price alert. We email you when that tool changes its price, credits, or free plan, and you get Keep, Test, Cut, the weekly letter." : "Confirm Keep, Test, Cut."} Nothing is added until you open this link.</p><p><a href="${link}">Confirm this address</a></p><p>Every email has an unsubscribe link.</p><p>AIToolsEssentials, 1090 West Foothill, Claremont, CA 91711.</p>`,
  });
  if (!mailed.ok) return page("Try again", "The confirm message did not send.");
  return page("Check your email", "Open the confirm link. The list stays empty until you do.");
}

// Best effort: a missing price_watch property in Resend must not break signup.
async function recordWatch(env, encoded, known, slug) {
  const current = known && known.properties ? known.properties[WATCH_PROPERTY] : "";
  const merged = mergeWatch(current, slug);
  try {
    await resend(env, `/contacts/${encoded}`, "PATCH", { properties: { [WATCH_PROPERTY]: merged } });
  } catch {
    // Signup continues without the watch.
  }
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
  return page("You are confirmed", "Keep, Test, Cut will include this address from the next approved issue.");
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "POST" && (url.pathname === "/" || url.pathname === "")) {
      return startSignup(request, env);
    }
    if (request.method === "GET" && url.pathname === "/confirm") return confirm(url, env);
    return page("Keep, Test, Cut", "Use the subscribe form on AIToolsEssentials.");
  },
};
