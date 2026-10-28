// Click each linked task of Mermaid diagrams in a running page, and report what each click opens.
//
// A Gantt diagram binds a task's link as a click handler that calls
// `window.open` once the page runs, so the link is proven by a click
// rather than by an anchor in a drawing. This program renders each
// diagram it reads with the Mermaid and the headless browser mermaid-cli
// ships, binds the handlers the render returns as a page embedding the
// diagram does, clicks the bar of each task Mermaid marks clickable, and
// records every URL `window.open` receives for that click.
//
// The one argument names mermaid-cli's `mmdc`, as a path or as a command
// on `PATH`; the browser and Mermaid are resolved from the package it
// belongs to, so the render runs offline under the versions mermaid-cli
// pins. Standard input holds a JSON array of diagram definitions, and
// standard output a JSON array holding, for each diagram, one array per
// click of the URLs it opened.

import { accessSync, constants, readFileSync, realpathSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

const TASK = ".task.clickable";
const PUPPETEER = { args: ["--no-sandbox"] };

function located(command) {
  if (command.includes(path.sep)) {
    return realpathSync(command);
  }
  for (const directory of (process.env.PATH ?? "").split(path.delimiter)) {
    const candidate = path.join(directory, command);
    try {
      accessSync(candidate, constants.X_OK);
      return realpathSync(candidate);
    } catch {
      continue;
    }
  }
  throw new Error(`${command} names no mermaid-cli command on PATH`);
}

async function clicked(page, mermaid, definition, at) {
  await page.setContent('<div id="container"></div>');
  await page.addScriptTag({ path: mermaid });
  await page.evaluate(
    async (definition, id) => {
      window.opened = [];
      window.open = (url) => {
        window.opened.push(url);
        return null;
      };
      globalThis.mermaid.initialize({ startOnLoad: false });
      const container = document.getElementById("container");
      const { svg, bindFunctions } = await globalThis.mermaid.render(id, definition);
      container.innerHTML = svg;
      bindFunctions?.(container);
    },
    definition,
    `diagram-${at}`,
  );
  const opened = [];
  for (const task of await page.$$(TASK)) {
    await page.evaluate(() => {
      window.opened = [];
    });
    await task.click();
    opened.push(await page.evaluate(() => window.opened));
  }
  return opened;
}

const require = createRequire(located(process.argv[2]));
const puppeteer = require("puppeteer");
const mermaid = require.resolve("mermaid/dist/mermaid.min.js");
const definitions = JSON.parse(readFileSync(0, "utf8"));
const browser = await puppeteer.launch(PUPPETEER);
try {
  const page = await browser.newPage();
  const report = [];
  for (const [at, definition] of definitions.entries()) {
    report.push(await clicked(page, mermaid, definition, at));
  }
  process.stdout.write(`${JSON.stringify(report)}\n`);
} finally {
  await browser.close();
}
