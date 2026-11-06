import { describe, expect, it } from "vitest";

import { buildAdminNav, type AdminNavCaps } from "../admin-nav";

const noCaps: AdminNavCaps = {
  canReadUsers: false,
  canReadFiles: false,
  canReadActivities: false,
  canReadSupport: false,
  canReadBroadcasts: false,
  canReadSystemSettings: false,
  canReadAdmins: false,
};

const itemKeys = (caps: AdminNavCaps): string[] =>
  buildAdminNav(caps).flatMap((section) => section.items.map((item) => item.key));

describe("buildAdminNav", () => {
  it("shows the admins entry to an account holding admins:read", () => {
    expect(itemKeys({ ...noCaps, canReadAdmins: true })).toContain("admins");
  });

  it("hides the admins entry without admins:read", () => {
    expect(itemKeys({ ...noCaps, canReadUsers: true })).not.toContain("admins");
  });

  it("drops a section left without any item", () => {
    const sections = buildAdminNav(noCaps).map((section) => section.key);
    expect(sections).toEqual(["overview", "account"]);
  });
});
