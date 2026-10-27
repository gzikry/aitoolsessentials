/* 30-second bill slasher. Seat prices are the amounts a visitor still pays,
   including grandfathered rungs. Overlap waste is the annual price of every
   extra seat in the same job. It is not a measured token bill. */
(function (root) {
  "use strict";

  var SEATS = [
    { id: "chatgpt", name: "ChatGPT Plus", price: 20, group: "chat", slug: "chatgpt" },
    { id: "claude", name: "Claude Pro", price: 20, group: "chat", slug: "claude" },
    { id: "claude-max", name: "Claude Code Max", price: 100, group: "chat", slug: "claude", replaces: ["claude", "claude-code"] },
    { id: "claude-code", name: "Claude Code", price: 20, group: "chat", slug: "claude", replaces: ["claude"] },
    { id: "cursor", name: "Cursor Pro", price: 20, group: "code", slug: "cursor" },
    { id: "copilot", name: "GitHub Copilot", price: 10, group: "code", slug: "github-copilot" },
    { id: "windsurf", name: "Windsurf", price: 15, group: "code", slug: "windsurf" },
    { id: "v0", name: "v0", price: 20, group: "builder", slug: "v0", trap: "v0 monthly credits expire after 65 days. Purchased credits lock if the paid plan lapses." },
    { id: "bolt", name: "Bolt.new", price: 25, group: "builder", slug: "bolt-new", trap: "Bolt.new Pro is $25/mo for 10M tokens, and the 25 Oct 2026 check says that allowance rolls over." },
    { id: "lovable", name: "Lovable", price: 25, group: "builder", slug: "lovable", trap: "Lovable monthly credits expire after 2 months. Daily grants do not roll over." },
    { id: "replit", name: "Replit Core", price: 20, group: "builder", slug: "replit-ai" },
    { id: "perplexity", name: "Perplexity Pro", price: 20, group: "chat", slug: "perplexity" },
    { id: "midjourney", name: "Midjourney", price: 10, group: "image", slug: "midjourney" },
    { id: "elevenlabs", name: "ElevenLabs", price: 22, group: "voice", slug: "elevenlabs", partner: true },
    { id: "descript", name: "Descript", price: 24, group: "video", slug: "descript", partner: true },
    { id: "notion", name: "Notion AI", price: 10, group: "docs", slug: "notion-ai" }
  ];

  var BY_ID = {};
  SEATS.forEach(function (seat) { BY_ID[seat.id] = seat; });

  function money(amount) {
    return "$" + String(amount).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function quote(ids) {
    var selected = SEATS.filter(function (seat) { return ids.indexOf(seat.id) !== -1; });
    var dropped = {};
    selected.forEach(function (seat) {
      (seat.replaces || []).forEach(function (id) {
        if (ids.indexOf(id) !== -1) dropped[id] = true;
      });
    });
    var active = selected.filter(function (seat) { return !dropped[seat.id]; });
    var monthly = active.reduce(function (sum, seat) { return sum + seat.price; }, 0);
    var groups = {};
    active.forEach(function (seat) {
      if (!groups[seat.group]) groups[seat.group] = [];
      groups[seat.group].push(seat);
    });
    var keep = [];
    var cut = [];
    var traps = [];
    Object.keys(groups).forEach(function (name) {
      var rows = groups[name].slice().sort(function (a, b) { return a.price - b.price; });
      if (rows.length === 1) {
        keep.push(rows[0]);
      } else {
        keep.push(rows[0]);
        rows.slice(1).forEach(function (seat) { cut.push(seat); });
      }
    });
    selected.forEach(function (seat) {
      if (seat.trap && traps.indexOf(seat.trap) === -1) traps.push(seat.trap);
    });
    var waste = cut.reduce(function (sum, seat) { return sum + seat.price * 12; }, 0);
    Object.keys(dropped).forEach(function (id) {
      var seat = BY_ID[id];
      if (seat && cut.indexOf(seat) === -1) {
        cut.push(seat);
        waste += seat.price * 12;
      }
    });
    return {
      monthly: monthly,
      annual: monthly * 12,
      waste: waste,
      keep: keep,
      cut: cut,
      traps: traps
    };
  }

  function link(seat, verb) {
    var rel = seat.partner ? ' rel="sponsored nofollow noopener"' : "";
    return '<a href="/go/' + seat.slug + '/"' + rel + ">" + verb + " " + seat.name + "</a>";
  }

  function render(result) {
    var lines = result.keep.map(function (seat) {
      return "<li><span>[KEEP]</span> " + seat.name + " <span>" + money(seat.price) + "/mo</span> " + link(seat, "Switch to") + "</li>";
    }).join("");
    var cuts = result.cut.map(function (seat) {
      return "<li><span>[CUT — SAVE " + money(seat.price * 12) + "/YR]</span> " + seat.name + "</li>";
    }).join("");
    var traps = result.traps.length
      ? "<p class=\"ledger-trap\">" + result.traps.join(" ") + "</p>"
      : "";
    var empty = result.keep.length ? "" : "<p>Tap the seats you pay for. The receipt stays in this browser.</p>";
    return (
      '<p class="ledger-total"><span>Monthly bill</span><strong data-monthly="' + result.monthly + '">' + money(result.monthly) + "/mo</strong></p>" +
      '<p class="ledger-total"><span>Annual spend</span><strong data-annual="' + result.annual + '">' + money(result.annual) + "/yr</strong></p>" +
      '<p class="ledger-total ledger-waste"><span>Estimated annual overlap waste</span><strong data-waste="' + result.waste + '">' + money(result.waste) + "/yr</strong></p>" +
      traps + empty +
      (lines ? "<ul class=\"ledger-lines\">" + lines + "</ul>" : "") +
      (cuts ? "<ul class=\"ledger-lines ledger-cuts\">" + cuts + "</ul>" : "") +
      '<p class="ledger-next"><a href="/compare/ai-coding-assistants/">Price the coding seats</a> · <a href="/compare/ai-app-builders/">Price the app builders</a> · <a href="/stack-audit.html">Open the full stack audit</a></p>'
    );
  }

  function read(form) {
    var ids = [];
    var boxes = form.querySelectorAll('input[name="bill-seat"]');
    Array.prototype.forEach.call(boxes, function (box) {
      if (box.checked) ids.push(box.value);
    });
    return ids;
  }

  function bind(doc) {
    doc = doc || document;
    var form = doc.getElementById("bill-slasher");
    var out = doc.getElementById("bill-result");
    if (!form || !out) return;
    function update() {
      out.innerHTML = render(quote(read(form)));
    }
    form.addEventListener("change", update);
    update();
  }

  root.BillSlasher = { seats: SEATS, quote: quote, render: render, bind: bind };
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () { bind(document); });
    } else {
      bind(document);
    }
  }
})(typeof window !== "undefined" ? window : globalThis);
