import type { ComparisonResult } from "./analysis";

const DB_NAME = "readability-analysis";
const DB_VERSION = 1;
const STORE_NAME = "results";

export interface StoredResult {
	name: string;
	url: string;
	result: ComparisonResult;
	timestamp: number;
}

function openDB(): Promise<IDBDatabase> {
	return new Promise((resolve, reject) => {
		if (typeof indexedDB === "undefined") {
			reject(new Error("IndexedDB not available"));
			return;
		}

		const request = indexedDB.open(DB_NAME, DB_VERSION);

		request.onerror = () => reject(request.error);
		request.onsuccess = () => resolve(request.result);

		request.onupgradeneeded = (event) => {
			const db = (event.target as IDBOpenDBRequest).result;
			if (!db.objectStoreNames.contains(STORE_NAME)) {
				db.createObjectStore(STORE_NAME, { keyPath: "name" });
			}
		};
	});
}

export async function saveResults(results: StoredResult[]): Promise<void> {
	const db = await openDB();

	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORE_NAME], "readwrite");
		const store = transaction.objectStore(STORE_NAME);

		store.clear();

		for (const result of results) {
			store.add(result);
		}

		transaction.oncomplete = () => {
			db.close();
			resolve();
		};
		transaction.onerror = () => {
			db.close();
			reject(transaction.error);
		};
	});
}

export async function loadResults(): Promise<StoredResult[]> {
	const db = await openDB();

	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORE_NAME], "readonly");
		const store = transaction.objectStore(STORE_NAME);
		const request = store.getAll();

		request.onsuccess = () => {
			db.close();
			resolve(request.result as StoredResult[]);
		};
		request.onerror = () => {
			db.close();
			reject(request.error);
		};
	});
}

export async function clearResults(): Promise<void> {
	const db = await openDB();

	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORE_NAME], "readwrite");
		const store = transaction.objectStore(STORE_NAME);
		const request = store.clear();

		request.onsuccess = () => {
			db.close();
			resolve();
		};
		request.onerror = () => {
			db.close();
			reject(request.error);
		};
	});
}
