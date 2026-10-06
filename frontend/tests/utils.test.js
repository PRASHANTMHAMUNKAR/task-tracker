import { test } from "node:test";
import assert from "node:assert/strict";
import { cleanTitle, isValidTitle } from "../src/utils.js";

test("cleanTitle trims whitespace", () => {
  assert.equal(cleanTitle("  hello  "), "hello");
});

test("isValidTitle rejects empty and too long", () => {
  assert.equal(isValidTitle("   "), false);
  assert.equal(isValidTitle("x".repeat(101)), false);
  assert.equal(isValidTitle("ok"), true);
});
