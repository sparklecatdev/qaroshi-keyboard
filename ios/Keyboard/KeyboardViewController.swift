import UIKit

final class KeyboardViewController: UIInputViewController {
    private let model = QaroshiModel()
    private let layoutNames = ["qwerty","azerty","dvorak"]
    private var layoutName = "qwerty"
    private var shifted = true
    private var locked = false
    private var numerals = false
    private var lastShiftTime: TimeInterval = 0
    private var lastSpaceTime: TimeInterval = 0
    private var lastOutput = ""
    private var undoRaw = ""
    private var undoCorrected = ""
    private let stack = UIStackView()
    private let suggestionsRow = UIStackView()
    private let backgroundColor = UIColor(red: 0.92, green: 0.94, blue: 0.97, alpha: 1)
    private var word: String {
        let text = textDocumentProxy.documentContextBeforeInput ?? ""
        let pattern = #"[a-zë]+(?:-[a-zë]+)*$"#
        guard let range = text.range(of: pattern, options: [.regularExpression, .caseInsensitive]) else { return "" }
        return String(text[range])
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        layoutName = UserDefaults.standard.string(forKey: "layout") ?? "qwerty"
        if !layoutNames.contains(layoutName) { layoutName = "qwerty" }
        stack.axis = .vertical; stack.spacing = 5
        stack.distribution = .fillEqually
        stack.translatesAutoresizingMaskIntoConstraints = false
        view.backgroundColor = backgroundColor
        view.addSubview(stack)
        NSLayoutConstraint.activate([
            stack.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 3),
            stack.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -3),
            stack.topAnchor.constraint(equalTo: view.topAnchor, constant: 4),
            stack.bottomAnchor.constraint(equalTo: view.bottomAnchor, constant: -5),
            view.heightAnchor.constraint(greaterThanOrEqualToConstant: 256)
        ])
        render()
    }
    override func textDidChange(_ textInput: UITextInput?) {
        super.textDidChange(textInput)
        updateSuggestions()
    }
    private var supportsSuggestions: Bool {
        switch textDocumentProxy.keyboardType {
        case .emailAddress, .URL, .numberPad, .phonePad, .decimalPad, .namePhonePad:
            return false
        default:
            return textDocumentProxy.autocorrectionType != .no
        }
    }
    private func button(_ title: String, flexible: CGFloat = 1, action: @escaping () -> Void) -> UIView {
        let b = UIButton(type: .system)
        b.setTitle(title, for: .normal)
        b.titleLabel?.font = .systemFont(ofSize: title.count > 3 ? 13 : 19, weight: .medium)
        b.backgroundColor = UIColor.white
        b.layer.cornerRadius = 7
        b.setTitleColor(.darkText, for: .normal)
        b.addAction(UIAction { _ in action() }, for: .touchUpInside)
        b.heightAnchor.constraint(greaterThanOrEqualToConstant: 41).isActive = true
        // Relative widths are applied within the row.
        b.widthAnchor.constraint(greaterThanOrEqualToConstant: flexible * 18).isActive = true
        return b
    }
    private func row(_ views: [UIView]) -> UIStackView {
        let s = UIStackView(arrangedSubviews: views)
        s.axis = .horizontal;s.alignment = .fill;s.distribution = .fillEqually;s.spacing = 4
        return s
    }
    private func clearRows() {
        for v in stack.arrangedSubviews { stack.removeArrangedSubview(v);v.removeFromSuperview() }
    }
    private func render() {
        clearRows()
        suggestionsRow.axis = .horizontal;suggestionsRow.spacing = 5
        suggestionsRow.distribution = .fillEqually
        stack.addArrangedSubview(suggestionsRow)
        updateSuggestions()
        if numerals {
            for chars in ["1234567890","@#$%&-+()",".,?!:;'/"] {
                stack.addArrangedSubview(row(chars.map { key in
                    let s = String(key);return button(s) { [weak self] in self?.insert(s) }
                }))
            }
        } else {
            let rows = model.rows(for: layoutName)
            for (index, keys) in rows.enumerated() {
                var buttons: [UIView] = []
                if index == 2 {
                    buttons.append(button(locked ? "⇪" : "⇧") { [weak self] in self?.toggleShift() })
                }
                for key in keys {
                    let out = model.output(key, shifted: shifted || locked)
                    buttons.append(button(out) { [weak self] in self?.insert(out) })
                }
                if index == 2 {
                    buttons.append(button("⌫") { [weak self] in self?.backspace() })
                }
                stack.addArrangedSubview(row(buttons))
            }
        }
        let bottom: [UIView] = [
            button(numerals ? "ABC" : "123") { [weak self] in
                guard let self else { return }
                self.numerals.toggle();self.render()
            },
            button(layoutName.uppercased()) { [weak self] in self?.nextLayout() },
            button("🌐") { [weak self] in self?.advanceToNextInputMode() },
            button("space",flexible:4) { [weak self] in self?.space() },
            button("↵") { [weak self] in self?.insert("\n") },
            button("⌫") { [weak self] in self?.backspace() }
        ]
        stack.addArrangedSubview(row(bottom))
    }
    private func toggleShift() {
        let time = Date().timeIntervalSince1970
        if shifted && time - lastShiftTime < 0.45 {
            locked.toggle();shifted = locked
        } else if locked { locked = false;shifted = false }
        else { shifted.toggle() }
        lastShiftTime = time;render()
    }
    private func nextLayout() {
        let i = layoutNames.firstIndex(of: layoutName) ?? 0
        layoutName = layoutNames[(i+1)%layoutNames.count]
        UserDefaults.standard.set(layoutName, forKey:"layout")
        render()
    }
    private func insert(_ output: String) {
        if output == " " { space();return }
        textDocumentProxy.insertText(output)
        undoRaw = "";undoCorrected = "";lastOutput = output
        lastSpaceTime = 0
        if shifted && !locked && output.first?.isLetter == true {
            shifted = false;render()
        } else { updateSuggestions() }
    }
    private func delete(_ count: Int) {
        for _ in 0..<count { textDocumentProxy.deleteBackward() }
    }
    private func space() {
        let now=Date().timeIntervalSince1970
        let before = textDocumentProxy.documentContextBeforeInput ?? ""
        if before.hasSuffix(" ") && now-lastSpaceTime < 0.65 {
            delete(1)
            textDocumentProxy.insertText(". ")
            lastSpaceTime=0;shifted=true;undoRaw="";undoCorrected=""
            render();return
        }
        undoRaw = "";undoCorrected = ""
        let typed = word
        if supportsSuggestions && !typed.isEmpty {
            let corrected = model.correction(typed)
            if typed != corrected {
                delete(typed.count)
                textDocumentProxy.insertText(corrected)
                undoRaw=typed;undoCorrected=corrected
            }
        }
        textDocumentProxy.insertText(" ")
        lastSpaceTime=now;lastOutput=""
        updateSuggestions()
    }
    private func backspace() {
        let before = textDocumentProxy.documentContextBeforeInput ?? ""
        if !undoRaw.isEmpty && before.hasSuffix(undoCorrected+" ") {
            delete(undoCorrected.count+1)
            textDocumentProxy.insertText(undoRaw+" ")
            undoRaw="";undoCorrected=""
        } else if lastOutput.count > 1 && before.hasSuffix(lastOutput) {
            delete(lastOutput.count)
        } else {
            textDocumentProxy.deleteBackward()
        }
        lastOutput="";lastSpaceTime=0;updateSuggestions()
    }
    private func choose(_ suggestion: String) {
        let original = word
        guard !original.isEmpty else { return }
        delete(original.count)
        let output = original.first?.isUppercase == true ?
            suggestion.prefix(1).uppercased() + suggestion.dropFirst() : suggestion
        textDocumentProxy.insertText(output)
        undoRaw="";undoCorrected=""
        updateSuggestions()
    }
    private func updateSuggestions() {
        for v in suggestionsRow.arrangedSubviews {suggestionsRow.removeArrangedSubview(v);v.removeFromSuperview()}
        let options = supportsSuggestions ? model.suggestions(for: word) : []
        if options.isEmpty {
            suggestionsRow.addArrangedSubview(button("Qaroshi • "+layoutName.uppercased()) {})
        } else {
            for candidate in options {
                suggestionsRow.addArrangedSubview(button(candidate) { [weak self] in self?.choose(candidate) })
            }
        }
    }
}
