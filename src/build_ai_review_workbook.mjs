import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = new URL("../", import.meta.url).pathname.replace(/^\/(.:)/, "$1");
const outputPath = `${root}data/validation/ai_assisted_review_v1.xlsx`;
const previewDir = `${root}reports/tmp`;

async function csvRows(path) {
  const text = await fs.readFile(path, "utf8");
  const wb = await Workbook.fromCSV(text, { sheetName: "Imported" });
  const values = wb.worksheets.getItem("Imported").getUsedRange().values;
  const headers = values[0].map(String);
  return values.slice(1).map((row) => Object.fromEntries(headers.map((header, index) => [header, row[index] == null ? "" : String(row[index])])))
}

const sample = await csvRows(`${root}data/validation/independent_review_sample_v1.csv`);
const registryRows = await csvRows(`${root}data/derived/model_dataset_exposure_development.csv`);
const assertionRows = await csvRows(`${root}data/curated/model_dataset_assertions.csv`);
const disjointRows = await csvRows(`${root}data/curated/documented_disjoint.csv`);
const datasetRows = await csvRows(`${root}data/curated/datasets.csv`);

const registry = new Map(registryRows.map((row) => [`${row.model_id}|${row.evaluation_dataset_id}`, row]));
const assertionsByModel = new Map();
for (const row of assertionRows) {
  if (!assertionsByModel.has(row.model_id)) assertionsByModel.set(row.model_id, []);
  assertionsByModel.get(row.model_id).push(row);
}
const disjoint = new Map(disjointRows.map((row) => [`${row.model_id}|${row.evaluation_dataset_id}`, row]));
const parent = new Map(datasetRows.filter((row) => row.parent_dataset_id).map((row) => [row.dataset_id, row.parent_dataset_id]));

function ancestors(datasetId) {
  const result = new Set();
  let current = datasetId;
  while (parent.has(current)) {
    current = parent.get(current);
    if (result.has(current)) throw new Error(`Dataset lineage cycle involving ${datasetId}`);
    result.add(current);
  }
  return result;
}

function aiReview(row) {
  const key = `${row.model_id}|${row.evaluation_dataset_id}`;
  const modelAssertions = assertionsByModel.get(row.model_id) ?? [];
  const exact = modelAssertions.filter((item) => item.dataset_id === row.evaluation_dataset_id);
  const parentMatches = modelAssertions.filter((item) => ancestors(row.evaluation_dataset_id).has(item.dataset_id));
  const excluded = disjoint.get(key);
  if (exact.length) {
    return {
      aiClass: "D3_exact_dataset_exposure",
      strength: exact.map((item) => item.evidence_strength).sort()[0],
      sources: [...new Set(exact.map((item) => item.source_url))].sort().join("; "),
      note: `Primary-source assertion(s) ${exact.map((item) => item.assertion_id).join(", ")} explicitly name the evaluation dataset in model development.`,
    };
  }
  if (parentMatches.length) {
    return {
      aiClass: "D2_parent_repository_exposure",
      strength: "C_lineage_inference",
      sources: [...new Set(parentMatches.map((item) => item.source_url))].sort().join("; "),
      note: `Primary-source assertion(s) ${parentMatches.map((item) => item.assertion_id).join(", ")} name an ancestor repository in the frozen lineage graph; exact slide exposure remains unresolved.`,
    };
  }
  if (excluded) {
    return {
      aiClass: "D0_documented_disjoint",
      strength: excluded.evidence_strength,
      sources: excluded.evidence_url,
      note: "A version-relevant primary-source statement documents exclusion of the named evaluation dataset.",
    };
  }
  return {
    aiClass: "D1_no_detected_evidence_or_insufficient_disclosure",
    strength: "D_incomplete_or_ambiguous_disclosure",
    sources: [...new Set(modelAssertions.map((item) => item.source_url))].sort().join("; "),
    note: "The frozen primary-source assertions for this model contained no exact dataset, ancestor-repository, identifier-overlap, or documented-disjoint evidence for this evaluation dataset. Independence cannot be assumed.",
  };
}

const reviewed = sample.map((row) => {
  const key = `${row.model_id}|${row.evaluation_dataset_id}`;
  const original = registry.get(key);
  if (!original) throw new Error(`Registry pair missing: ${key}`);
  const review = aiReview(row);
  return {
    auditRow: Number(row.audit_row),
    modelId: row.model_id,
    modelName: row.model_name,
    evaluationDatasetId: row.evaluation_dataset_id,
    developmentClass: original.exposure_scope,
    aiReviewClass: review.aiClass,
    agreement: original.exposure_scope === review.aiClass ? "Yes" : "No",
    aiEvidenceStrength: review.strength,
    aiSourceUrls: review.sources,
    aiEvidenceNote: review.note,
    reviewerLabel: "OpenAI Codex GPT-5.6 Sol (AI-assisted verification)",
    reviewDate: "2026-09-28",
    initiallyBlinded: "No",
    independenceLimit: "AI verification; not independent human validation and not a gold-standard accuracy estimate.",
  };
});

const agreements = reviewed.filter((row) => row.agreement === "Yes").length;
const classCounts = new Map();
for (const row of reviewed) classCounts.set(row.aiReviewClass, (classCounts.get(row.aiReviewClass) ?? 0) + 1);

const workbook = Workbook.create();
const summary = workbook.worksheets.add("Summary");
const review = workbook.worksheets.add("AI review");
summary.showGridLines = false;
review.showGridLines = false;

summary.getRange("A2:F2").merge();
summary.getRange("A2").values = [["OncoPretrainMap AI-assisted review"]];
summary.getRange("A2:F2").format.font = { name: "Arial", size: 16, bold: true, color: "#1F2937" };
summary.getRange("A4:F5").merge();
summary.getRange("A4").values = [["OpenAI Codex GPT-5.6 Sol reviewed the frozen 80-pair sample using the project’s primary-source assertions, disjointness records, and dataset-lineage rules. The AI had access to the project repository. This is an AI-assisted verification, not independent human validation."]];
summary.getRange("A4:F5").format = { font: { name: "Arial", size: 10, color: "#374151", italic: true }, wrapText: true, verticalAlignment: "center" };
summary.getRange("A7:B12").values = [
  ["Measure", "Result"],
  ["Pairs reviewed", reviewed.length],
  ["Exact agreement", agreements],
  ["Agreement proportion", agreements / reviewed.length],
  ["Disagreements", reviewed.length - agreements],
  ["Independent human validation", "Not completed"],
];
summary.getRange("D7:E12").values = [
  ["AI review class", "Count"],
  ["D0 documented disjoint", classCounts.get("D0_documented_disjoint") ?? 0],
  ["D1 unresolved", classCounts.get("D1_no_detected_evidence_or_insufficient_disclosure") ?? 0],
  ["D2 parent repository", classCounts.get("D2_parent_repository_exposure") ?? 0],
  ["D3 exact dataset", classCounts.get("D3_exact_dataset_exposure") ?? 0],
  ["D4 exact identifiers", classCounts.get("D4_exact_case_slide_or_patch_overlap") ?? 0],
];
for (const rangeAddress of ["A7:B7", "D7:E7"]) {
  summary.getRange(rangeAddress).format = { fill: "#24506A", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center" };
}
summary.getRange("A8:A12").format.font = { name: "Arial", size: 10, color: "#1F2937" };
summary.getRange("B8:B12").format.font = { name: "Arial", size: 10, color: "#1F2937" };
summary.getRange("D8:E12").format.font = { name: "Arial", size: 10, color: "#1F2937" };
summary.getRange("B10").format.numberFormat = "0.0%";
summary.getRange("A7:B12").format.borders = { preset: "outside", style: "thin", color: "#CBD5E1" };
summary.getRange("D7:E12").format.borders = { preset: "outside", style: "thin", color: "#CBD5E1" };
summary.getRange("A14:F15").merge();
summary.getRange("A14").values = [["Interpretation: complete concordance shows that the frozen software rules reproduce the development classifications from the same curated evidence. It does not measure independent curator reliability, source truth, or model contamination."]];
summary.getRange("A14:F15").format = { fill: "#FEF3C7", font: { name: "Arial", size: 10, color: "#78350F" }, wrapText: true, verticalAlignment: "center" };
summary.getRange("A1:F16").format.verticalAlignment = "center";
summary.getRange("A1:F16").format.columnWidth = 18;
summary.getRange("A:A").format.columnWidth = 29;
summary.getRange("B:B").format.columnWidth = 20;
summary.getRange("C:C").format.columnWidth = 3;
summary.getRange("D:D").format.columnWidth = 29;
summary.getRange("E:E").format.columnWidth = 14;

const headers = [
  "audit_row", "model_id", "model_name", "evaluation_dataset_id", "development_class",
  "ai_review_class", "agreement", "ai_evidence_strength", "ai_source_urls", "ai_evidence_note",
  "reviewer_label", "review_date", "initially_blinded", "independence_limit",
];
const values = reviewed.map((row) => [
  row.auditRow, row.modelId, row.modelName, row.evaluationDatasetId, row.developmentClass,
  row.aiReviewClass, row.agreement, row.aiEvidenceStrength, row.aiSourceUrls, row.aiEvidenceNote,
  row.reviewerLabel, row.reviewDate, row.initiallyBlinded, row.independenceLimit,
]);
review.getRange("A1:N81").values = [headers, ...values];
review.getRange("A1:N1").format = { fill: "#24506A", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true };
review.getRange("A2:N81").format = { font: { name: "Arial", size: 9, color: "#1F2937" }, verticalAlignment: "top" };
review.getRange("A2:A81").format.numberFormat = "0";
review.getRange("A:A").format.columnWidth = 10;
review.getRange("B:B").format.columnWidth = 22;
review.getRange("C:C").format.columnWidth = 24;
review.getRange("D:D").format.columnWidth = 25;
review.getRange("E:F").format.columnWidth = 35;
review.getRange("G:G").format.columnWidth = 11;
review.getRange("H:H").format.columnWidth = 34;
review.getRange("I:I").format.columnWidth = 52;
review.getRange("J:J").format.columnWidth = 58;
review.getRange("K:K").format.columnWidth = 38;
review.getRange("L:M").format.columnWidth = 14;
review.getRange("N:N").format.columnWidth = 58;
review.getRange("I2:N81").format.wrapText = true;
review.freezePanes.freezeRows(1);
review.freezePanes.freezeColumns(4);
const table = review.tables.add("A1:N81", true, "AIReviewTable");
table.style = "TableStyleMedium2";
table.showBandedRows = true;

workbook.recalculate();
const summaryInspect = await workbook.inspect({ kind: "table", sheetId: "Summary", range: "A2:F15", include: "values,formulas", tableMaxRows: 20, tableMaxCols: 8, maxChars: 8000 });
const reviewInspect = await workbook.inspect({ kind: "table", sheetId: "AI review", range: "A1:N8", include: "values,formulas", tableMaxRows: 8, tableMaxCols: 14, maxChars: 12000 });
const errorInspect = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" });
console.log(summaryInspect.ndjson);
console.log(reviewInspect.ndjson);
console.log(errorInspect.ndjson);

await fs.mkdir(previewDir, { recursive: true });
const summaryPreview = await workbook.render({ sheetName: "Summary", range: "A1:F16", scale: 1.5, format: "png" });
await fs.writeFile(`${previewDir}/ai_review_summary.png`, new Uint8Array(await summaryPreview.arrayBuffer()));
const reviewPreview = await workbook.render({ sheetName: "AI review", range: "A1:N12", scale: 0.8, format: "png" });
await fs.writeFile(`${previewDir}/ai_review_rows.png`, new Uint8Array(await reviewPreview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(JSON.stringify({ outputPath, rows: reviewed.length, agreements, disagreements: reviewed.length - agreements, initiallyBlinded: false }, null, 2));
