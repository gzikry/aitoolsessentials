/* App-builder seat and credit-burn calculator.
   Prices checked 25 Oct 2026 on the vendors' pricing pages.
   Runs in the browser. No login, no network. */
(function (root) {
  "use strict";

  var SEATS = [
    { id: "legacy-v0", name: "Legacy v0 Premium", price: 20, group: "v0" },
    { id: "v0-plus", name: "v0 Plus", price: 30, group: "v0" },
    { id: "replit-core", name: "Replit Core", price: 20, group: "replit" },
    { id: "bolt-pro", name: "Bolt.new Pro", price: 25, group: "bolt" },
    { id: "lovable-pro", name: "Lovable Pro", price: 25, group: "lovable" }
  ];

  var BY_ID = {};
  SEATS.forEach(function (seat) { BY_ID[seat.id] = seat; });

  function money(amount) {
    return "$" + String(amount);
  }

  function seatLine(seat) {
    return seat.name + " (" + money(seat.price) + "/mo)";
  }

  function ordered(ids) {
    return SEATS.filter(function (seat) { return ids.indexOf(seat.id) !== -1; });
  }

  function recommend(selectedIds, cadence, activeId) {
    var selected = ordered(selectedIds || []);
    var ids = selected.map(function (seat) { return seat.id; });
    var monthly = selected.reduce(function (sum, seat) { return sum + seat.price; }, 0);
    var hasLegacy = ids.indexOf("legacy-v0") !== -1;
    var hasV0 = selected.some(function (seat) { return seat.group === "v0"; });
    var hasLovable = ids.indexOf("lovable-pro") !== -1;
    var keepIds = [];
    var cutIds = [];
    var test = [];
    var reason = "";

    if (cadence === "quarterly" || cadence === "idle") {
      test = [
        "Bolt.new Free (1M tokens/mo)",
        "Lovable Free (5 daily credits)"
      ];
      if (hasLegacy) {
        keepIds = ["legacy-v0"];
        cutIds = ids.filter(function (id) { return id !== "legacy-v0"; });
        reason = cadence === "idle"
          ? "No commit in 30 days is the cancel test for every seat except legacy v0 Premium. You already hold the $20 tier, and cancelling it means you cannot buy it back. Export the idle repos to GitHub and cut the other paid seats before renewal."
          : "A once-a-quarter prototype does not need a second paid builder. Keep legacy v0 Premium if you already hold it. Test Bolt.new Free or Lovable Free for the next UI, and cut the other paid seats before they renew.";
      } else {
        keepIds = [];
        cutIds = ids.slice();
        reason = cadence === "idle"
          ? "No commit in 30 days. Sync the repo to GitHub and cancel the paid app-builder seats before renewal. Bolt.new Free and Lovable Free stay open for the next prototype."
          : "You only spin up a UI once a quarter. Bolt.new Free (1M tokens/mo, 300K daily limit) and Lovable Free (5 daily credits, up to 30 a month) remain open. Export finished code to GitHub and cancel the idle paid seats before renewal.";
      }
    } else if (!ids.length) {
      test = [
        "Bolt.new Free (1M tokens/mo)",
        "Lovable Free (5 daily credits)"
      ];
      reason = "No paid app-builder seat is selected. Test Bolt.new Free or Lovable Free before you open a paid seat.";
    } else if (hasLegacy) {
      keepIds = ["legacy-v0"];
      cutIds = ids.filter(function (id) { return id !== "legacy-v0"; });
      test = [
        "Bolt.new Free (1M tokens/mo)",
        "Lovable Free (5 daily credits)"
      ];
      reason = cutIds.length
        ? "Keep legacy v0 Premium at $20/mo. It is closed to new signups, so cancelling it means Plus at $30/user/mo is the way back. Cut the other paid seats. A second paid builder is the overlap."
        : "Keep legacy v0 Premium at $20/mo while you are shipping. Do not add a second paid builder. Test Bolt.new Free or Lovable Free if you want a side prototype.";
    } else if (ids.length === 1) {
      keepIds = ids.slice();
      test = [
        "Bolt.new Free (1M tokens/mo)",
        "Lovable Free (5 daily credits)"
      ];
      reason = "One paid builder for the prototype you are shipping this month. That is the keep. Test Bolt.new Free or Lovable Free before you add another paid seat.";
    } else {
      var active = activeId && ids.indexOf(activeId) !== -1 ? activeId : ids[0];
      keepIds = [active];
      cutIds = ids.filter(function (id) { return id !== active; });
      test = [
        "Bolt.new Free (1M tokens/mo)",
        "Lovable Free (5 daily credits)"
      ];
      reason = "Keep at most one paid builder for the prototype you are shipping this month. The other paid seats are duplicate-seat waste. Test Bolt.new Free or Lovable Free instead of paying for a second one.";
    }

    var keepSeats = ordered(keepIds);
    var cutSeats = ordered(cutIds);
    var wasteMonthly = cutSeats.reduce(function (sum, seat) { return sum + seat.price; }, 0);
    var expiry = [];
    if (hasV0) {
      expiry.push("v0 top-ups and monthly credits expire after 65 days. Purchased credits lock if the paid plan lapses.");
    }
    if (hasLovable) {
      expiry.push("Lovable monthly credits expire after 2 months. Daily grants do not roll over.");
    }
    if (!expiry.length) {
      expiry.push("None of the seats you checked use the 65-day v0 window or the 2-month Lovable window. Those clocks still apply if you buy a v0 top-up or a Lovable monthly credit later.");
    }

    return {
      cadence: cadence || "shipping",
      monthly: monthly,
      annual: monthly * 12,
      wasteMonthly: wasteMonthly,
      wasteAnnual: wasteMonthly * 12,
      keep: keepSeats.map(seatLine),
      cut: cutSeats.map(seatLine),
      test: test,
      expiry: expiry,
      reason: reason
    };
  }

  function list(items, empty) {
    if (!items.length) return "<p>" + empty + "</p>";
    return "<ul>" + items.map(function (item) {
      return "<li>" + item + "</li>";
    }).join("") + "</ul>";
  }

  function render(result) {
    var keepEmpty = "No paid seat to keep.";
    var cutEmpty = "Nothing to cut. You are not paying for a second app-builder seat.";
    return (
      '<p class="app-builder-waste"><span>Annual duplicate-seat waste</span><strong data-waste="' +
      result.wasteAnnual + '">' + money(result.wasteAnnual) + "</strong></p>" +
      "<p>Selected seats cost " + money(result.monthly) + "/mo (" + money(result.annual) +
      "/yr). Waste is 12 times the monthly price of every selected seat except the one this call says to keep.</p>" +
      "<h3>Keep</h3>" + list(result.keep, keepEmpty) +
      "<h3>Test First</h3>" + list(result.test, "No free tier to test.") +
      "<h3>Cut</h3>" + list(result.cut, cutEmpty) +
      "<h3>Credit-expiry risk</h3>" + list(result.expiry, "") +
      "<p>" + result.reason + "</p>"
    );
  }

  function readForm(form) {
    var selected = [];
    var boxes = form.querySelectorAll('input[name="seat"]');
    Array.prototype.forEach.call(boxes, function (box) {
      if (box.checked) selected.push(box.value);
    });
    var cadenceInput = form.querySelector('input[name="cadence"]:checked');
    var cadence = cadenceInput ? cadenceInput.value : "shipping";
    var activeSelect = form.querySelector("#app-builder-active");
    var activeId = activeSelect ? activeSelect.value : "";
    return { selected: selected, cadence: cadence, activeId: activeId };
  }

  function syncActive(form, selected, cadence) {
    var wrap = form.querySelector("#app-builder-active-wrap");
    var select = form.querySelector("#app-builder-active");
    if (!wrap || !select) return;
    var legacy = selected.indexOf("legacy-v0") !== -1;
    var show = cadence === "shipping" && selected.length > 1 && !legacy;
    wrap.hidden = !show;
    if (!show) return;
    var previous = select.value;
    select.innerHTML = "";
    ordered(selected).forEach(function (seat) {
      var option = document.createElement("option");
      option.value = seat.id;
      option.textContent = seatLine(seat);
      select.appendChild(option);
    });
    if (previous && selected.indexOf(previous) !== -1) select.value = previous;
  }

  function bind(doc) {
    doc = doc || document;
    var form = doc.getElementById("app-builder-calc");
    var out = doc.getElementById("app-builder-result");
    if (!form || !out) return;
    function update() {
      var state = readForm(form);
      syncActive(form, state.selected, state.cadence);
      state = readForm(form);
      out.innerHTML = render(recommend(state.selected, state.cadence, state.activeId));
    }
    form.addEventListener("change", update);
    form.addEventListener("input", update);
    update();
  }

  root.AppBuilderCalc = { seats: SEATS, recommend: recommend, render: render, bind: bind };
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () { bind(document); });
    } else {
      bind(document);
    }
  }
})(typeof globalThis !== "undefined" ? globalThis : this);
