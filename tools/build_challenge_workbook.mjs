import fs from "node:fs/promises";
import path from "node:path";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const root = path.resolve(import.meta.dirname, "..");
const packet = JSON.parse(await fs.readFile(path.join(root, "data/validation/challenge80_packet_data_v1.json"), "utf8"));
if (packet.length !== 80 || new Set(packet.map((r) => r.review_id)).size !== 80) {
  throw new Error("Expected 80 unique review IDs");
}
const wb = Workbook.create();
const review = wb.worksheets.add("Blinded review");
const guide = wb.worksheets.add("Instructions");
review.showGridLines = false;
guide.showGridLines = false;

review.getRange("A1:P1").merge();
review.getRange("A1").values = [["OncoPretrainMap | 80-row blinded challenge review"]];
review.getRange("A1:P1").format.fill = "#17324D";
review.getRange("A1:P1").format.font = { name: "Aptos", size: 16, bold: true, color: "#FFFFFF" };
review.getRange("A1:P1").format.rowHeight = 32;
review.getRange("A2:P2").merge();
review.getRange("A2").values = [["Enter independent decisions in columns G-P. Do not consult the development registry or prior review workbooks until this file is returned."]];
review.getRange("A2:P2").format.font = { name: "Aptos", size: 11, color: "#31526E" };
review.getRange("A2:P2").format.rowHeight = 30;
review.getRange("A3:P3").merge();
review.getRange("A3").values = [["No initial exposure class, evidence grade, source assertion or adjudicated answer is supplied in this packet."]];
review.getRange("A3:P3").format.font = { name: "Aptos", size: 10, color: "#53687B" };
review.getRange("A3:P3").format.rowHeight = 24;

const headers = [
  "Review ID", "Benchmark context", "Model/checkpoint", "Evaluation dataset/task", "Evaluation institution",
  "Checkpoint/version resolved?", "Reviewer class D0–D4", "Evidence grade A–D", "Primary source URLs",
  "Source passage / evidence and containment reasoning", "Independent search log (including negative search)",
  "Overlap warning, if any", "Reviewer name", "Review date (YYYY-MM-DD)", "Blinded to registry answers?", "AI used for decisions?",
];
review.getRange("A5:P5").values = [headers];
review.getRange("A5:P5").format.fill = "#2A5976";
review.getRange("A5:P5").format.font = { name: "Aptos", size: 10, bold: true, color: "#FFFFFF" };
review.getRange("A5:P5").format.wrapText = true;
review.getRange("A5:P5").format.rowHeight = 43;
const rows = packet.map((r) => [
  r.review_id, r.benchmark_context, r.model_checkpoint, r.evaluation_dataset_or_task,
  r.evaluation_institution, "", "", "", "", "", "", "", "", "", "", "",
]);
review.getRange("A6:P85").values = rows;
review.getRange("A6:E85").format.fill = "#EEF3F7";
review.getRange("F6:P85").format.fill = "#FFFDF3";
review.getRange("A6:P85").format.font = { name: "Aptos", size: 10 };
review.getRange("A6:P85").format.rowHeight = 25;
review.getRange("A6:P85").format.borders = { preset: "inside", style: "thin", color: "#E1E7ED" };
for (const [col, width] of Object.entries({
  A: 14, B: 24, C: 22, D: 27, E: 18, F: 16, G: 17, H: 18,
  I: 32, J: 54, K: 48, L: 24, M: 19, N: 19, O: 18, P: 17,
})) review.getRange(`${col}:${col}`).format.columnWidth = width;
review.freezePanes.freezeRows(5);
review.getRange("F6:F85").dataValidation = { rule: { type: "list", values: ["Yes", "No", "Unclear"] } };
review.getRange("G6:G85").dataValidation = { rule: { type: "list", values: ["D0", "D1", "D2", "D3", "D4"] } };
review.getRange("H6:H85").dataValidation = { rule: { type: "list", values: ["A", "B", "C", "D"] } };
review.getRange("O6:P85").dataValidation = { rule: { type: "list", values: ["Yes", "No"] } };

guide.getRange("A1:D1").merge();
guide.getRange("A1").values = [["Reviewer instructions"]];
guide.getRange("A1:D1").format.fill = "#17324D";
guide.getRange("A1:D1").format.font = { name: "Aptos", size: 16, bold: true, color: "#FFFFFF" };
guide.getRange("A1:D1").format.rowHeight = 34;
const rules = [
  ["Purpose", "Independent source search and application of the frozen D0–D4 rules to 80 previously unreviewed relationships."],
  ["Blinding", "Do not open the public registry classification tables, old review files, private key, or manuscript result tables until your decisions are returned."],
  ["D0", "Version-specific source explicitly excludes the evaluation dataset/cohort from model development."],
  ["D1", "No public evidence establishes D0 or D2–D4. Missing disclosure is not independence."],
  ["D2", "A source establishes that the training corpus contains the repository/cohort from which this evaluation set was drawn; exact IDs unavailable."],
  ["D3", "The named evaluation dataset is explicitly included in model development; exact evaluated IDs not confirmed."],
  ["D4", "Released identifiers or equivalent evidence confirm the same evaluated case, slide, or patch was used in development."],
  ["Institution rule", "The same institution on both sides, without an established corpus-containment relationship, is D1 rather than D2. Record an overlap warning if relevant."],
  ["Evidence A", "Identifier manifest or exact ID-level evidence."],
  ["Evidence B", "Explicit checkpoint-specific primary-source statement."],
  ["Evidence C", "Dataset-lineage inference supported by public sources."],
  ["Evidence D", "Incomplete or ambiguous disclosure."],
  ["Search", "Find the primary model paper/model card, the evaluation benchmark source, and any public training manifests. Record what was searched even if no exposure was found."],
  ["Return", "Complete all 80 rows, retain the original decisions, and return the dated workbook before any comparison with the answer key."],
];
guide.getRange("A3:B16").values = rules;
guide.getRange("A3:A16").format.fill = "#E6EEF4";
guide.getRange("A3:A16").format.font = { name: "Aptos", size: 10, bold: true };
guide.getRange("B3:B16").format.font = { name: "Aptos", size: 10 };
guide.getRange("A3:B16").format.wrapText = true;
guide.getRange("A3:B16").format.rowHeight = 47;
guide.getRange("A:A").format.columnWidth = 20;
guide.getRange("B:B").format.columnWidth = 95;
guide.freezePanes.freezeRows(2);

wb.recalculate();
const check = await wb.inspect({ kind: "table", range: "Blinded review!A5:P8", include: "values,formulas", tableMaxRows: 4, tableMaxCols: 16 });
console.log(check.ndjson);
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!", options: { useRegex: true, maxResults: 20 } });
console.log(errors.ndjson);
const tmp = path.join(root, ".tmp_artifact");
await fs.mkdir(tmp, { recursive: true });
for (const [name, sheetName, range] of [
  ["challenge_review_preview.png", "Blinded review", "A1:J10"],
  ["challenge_instructions_preview.png", "Instructions", "A1:B16"],
]) {
  const preview = await wb.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(path.join(tmp, name), new Uint8Array(await preview.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(wb);
const outPath = path.join(root, "data/validation/challenge80_blinded_review_v1.xlsx");
await output.save(outPath);
console.log(outPath);
