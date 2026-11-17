import SwiftUI

@main
struct QaroshiApp: App {\n    @State private var sample = ""
    var body: some Scene {
        WindowGroup {
            NavigationStack {
                VStack(alignment: .leading, spacing: 18) {
                    Text("Qaroshi Keyboard")
                        .font(.largeTitle.bold())
                    Text("A private, offline Qaroshi keyboard with QWERTY, AZERTY and Dvorak layouts.")
                        .foregroundStyle(.secondary)
                    Text("1. Install this app through Xcode or TestFlight.\n2. Open Settings → General → Keyboard → Keyboards → Add New Keyboard.\n3. Enable Qaroshi Keyboard.\n4. Switch keyboards with the globe key and choose your layout inside Qaroshi.")
                    Text("Autocorrection is intentionally conservative and only uses the bundled Qaroshi lexicon. No Full Access or network permission is needed.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    TextField("Practice Qaroshi here", text: $sample)
                        .textInputAutocapitalization(.sentences)
                        .textFieldStyle(.roundedBorder)
                    Spacer()
                }
                .padding()
            }
        }
    }
}
