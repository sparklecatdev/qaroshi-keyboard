import Foundation

struct QaroshiModel {
    private(set) var rows: [String: [[String]]] = [:]
    private(set) var special: [String: String] = [:]
    private(set) var scores: [String: Int] = [:]
    init() {
        if let url = Bundle.main.url(forResource: "mapping", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let object = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
            rows = object["layoutRows"] as? [String: [[String]]] ?? [:]
            special = object["specialLetterReplacements"] as? [String: String] ?? [:]
        }
        if let url = Bundle.main.url(forResource: "qaroshi-lexicon", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let object = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
           let entries = object["words"] as? [[Any]] {
            for item in entries where item.count >= 2 {
                if let word = item[0] as? String, let score = item[1] as? Int {
                    scores[word] = score
                }
            }
        }
    }
    func output(_ s: String, shifted: Bool) -> String {
        let value = special[s] ?? s
        return shifted ? value.prefix(1).uppercased() + value.dropFirst() : value
    }
    func rows(for layout: String) -> [[String]] {
        rows[layout] ?? rows["qwerty"] ?? []
    }
    func oneEdit(_ a: String, _ b: String) -> Bool {
        if a == b { return true }
        if abs(a.count - b.count) > 1 { return false }
        let x = Array(a), y = Array(b)
        var i = 0
        while i < min(x.count, y.count) && x[i] == y[i] { i += 1 }
        if x.count == y.count {
            if Array(x.dropFirst(min(i+1,x.count))) == Array(y.dropFirst(min(i+1,y.count))) { return true }
            return i+1 < x.count && x[i] == y[i+1] && x[i+1] == y[i]
                && Array(x.dropFirst(i+2)) == Array(y.dropFirst(i+2))
        }
        if x.count > y.count { return Array(x.dropFirst(i+1)) == Array(y.dropFirst(i)) }
        return Array(x.dropFirst(i)) == Array(y.dropFirst(i+1))
    }
    private func valid(_ raw: String) -> Bool {
        guard !raw.isEmpty else { return false }
        return raw.range(of: #"^[a-zë]+(?:-[a-zë]+)*$"#, options: .regularExpression) != nil
    }
    func suggestions(for raw: String) -> [String] {
        let word = raw.lowercased().precomposedStringWithCanonicalMapping
        guard word.count <= 35 && valid(word) else { return [] }
        var result: [String] = scores[word] == nil ? [] : [word]
        let prefix = scores.keys.filter { $0.hasPrefix(word) && $0 != word }
            .sorted { (scores[$0] ?? 0) > (scores[$1] ?? 0) }
        for item in prefix where result.count < 3 { result.append(item) }
        if result.count < 3 && word.count >= 4 && !word.contains("-") {
            let near = scores.keys.filter {
                abs($0.count - word.count) <= 1 && !result.contains($0) && oneEdit(word,$0)
            }.sorted { (scores[$0] ?? 0) > (scores[$1] ?? 0) }
            for item in near where result.count < 3 { result.append(item) }
        }
        return result
    }
    func correction(_ raw: String) -> String {
        let word = raw.precomposedStringWithCanonicalMapping
        guard word.count >= 4 && !word.contains("-") && word == word.lowercased()
                && valid(word) && scores[word] == nil else { return raw }
        let near = scores.keys.filter {
            $0.count >= 4 && $0.count <= word.count+1 && oneEdit(word,$0)
        }.sorted { (scores[$0] ?? 0) > (scores[$1] ?? 0) }
        guard let first = near.first else { return raw }
        if near.count == 1 { return first }
        let high = scores[first] ?? 0, next = scores[near[1]] ?? 0
        return high >= 5000 && high >= 2*next ? first : raw
    }
}
