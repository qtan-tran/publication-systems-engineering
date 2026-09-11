# Publication Systems Engineering

**Publication Systems Engineering (PSE)** là một framework source-available để xây dựng các hệ thống sản xuất sách đáng tin cậy, có thể mở rộng và duy trì lâu dài.

PSE xem quy trình xuất bản như một vòng đời kỹ thuật, không phải tập hợp những template rời rạc:

`nội dung → siêu dữ liệu → cấu hình nhan đề → profile + mô-đun ngữ nghĩa → lõi → dựng sách → QA → proof/phát hành`

Mục tiêu production hiện tại được giữ có chủ đích ở phạm vi hẹp: **PDF sẵn sàng cho in bằng LuaLaTeX** trên Windows, macOS và Linux.

> **Trạng thái — 1.47.0-alpha:** technical beta candidate trong giai đoạn stabilization-only surface freeze (9 profiles / 14 semantic modules). Bề mặt repository công khai đã được làm sạch và các command/schema contract đã đóng băng, nhưng đây **chưa phải public licensed beta**. Independent legal review và live CI trên đúng release candidate vẫn là hard gate.

## Xem PSE tạo ra sách như thế nào

Bạn có thể mở PDF hoàn chỉnh trước khi cài đặt. Mọi demo đều dùng nội dung synthetic và cùng public build path của PSE.

| Profile | Phù hợp với | PDF demo |
| --- | --- | --- |
| `basic-book` | Sách văn xuôi thông thường | [Xem PDF](examples/profiles/basic-book/output/basic-book-demo.pdf) |
| `literary-fiction` | Tiểu thuyết và văn xuôi thiên về trải nghiệm đọc | [Xem PDF](examples/profiles/literary-fiction/output/literary-fiction-demo.pdf) |
| `academic-monograph` | Chuyên khảo nghiên cứu | [Xem PDF](examples/profiles/academic-monograph/output/academic-monograph-demo.pdf) |
| `scholarly-edition` | Ấn bản học thuật có chú giải | [Xem PDF](examples/profiles/scholarly-edition/output/scholarly-edition-demo.pdf) |
| `critical-edition` | Critical edition thiên về văn bản nguồn | [Xem PDF](examples/profiles/critical-edition/output/critical-edition-demo.pdf) |
| `drama` | Kịch bản sân khấu | [Xem PDF](examples/profiles/drama/output/drama-demo.pdf) |
| `bilingual-edition` | Ấn bản song ngữ song song | [Xem PDF](examples/profiles/bilingual-edition/output/bilingual-edition-demo.pdf) |
| `poetry` | Tuyển tập thơ | [Xem PDF](examples/profiles/poetry/output/poetry-demo.pdf) |
| `edited-collection` | Sách nhiều tác giả theo chương | [Xem PDF](examples/profiles/edited-collection/output/edited-collection-demo.pdf) |

Nếu chưa quen kỹ thuật, bắt đầu với [Beginner quick start](docs/getting-started/BEGINNER-QUICK-START.md), sau đó xem [Choose a profile](docs/getting-started/CHOOSE-A-PROFILE.md).

## PSE giải quyết vấn đề gì?

PSE dành cho biên tập viên, nhân sự dàn trang, nhóm xuất bản độc lập/quy mô nhỏ và scholarly editor cần:

- tính nhất quán cho cả series;
- core architecture tái sử dụng thay vì copy template;
- quy trình manuscript/proof an toàn theo mặc định;
- clean build và release artifact có khả năng kiểm chứng;
- kiểm thử hồi quy kết hợp với cổng kiểm của con người;
- profile chỉ phụ trách presentation, không sở hữu security hay semantic QA;
- semantic modules có thể kết hợp mà không viết lại backbone.

## Năng lực hiện có

Backbone alpha hiện bao gồm:

- `pse new` để tạo project an toàn;
- installed-runtime discovery và `pse doctor`;
- profile trung tính cho basic book, literary fiction, academic monograph, scholarly edition, critical edition, poetry, edited collection, drama và bilingual edition;
- semantic modules cho locator, apparatus, multilingual text, bibliography, index, scholarly matter, verse, drama và parallel text;
- parser semantic không thực thi TeX, có vị trí file/dòng/cột;
- `pse build`, `pse check`, visual/regression QA;
- `pse inspect-output` để kiểm baseline giới hạn về metadata/navigation/text extraction của PDF, không phải chứng nhận accessibility; release artifact bind inspection evidence vào đúng SHA-256 của final PDF;
- `pse proof` tạo proof watermark riêng theo người nhận;
- `pse release` tạo release có manifest và SHA-256, với deterministic local build;
- `pse verify-release` kiểm integrity/tampering.
- `pse contracts` để xem contract/schema đang được cài đặt, `pse release-migration` để đánh giá release cũ mà không sửa artifact lịch sử, và `pse audit-release` để tạo audit evidence riêng, gắn với hash của artifact quan sát được.
- `pse audit-index` creates an external portable batch audit index for a collection of releases.

Mọi fixture công khai đều là nội dung synthetic. PSE không chứa kiến trúc downstream riêng tư hay bản thảo chưa phát hành.

## Bắt đầu nhanh

Cài từ candidate checkout:

```text
python -m pip install .
pse doctor --deep
```

Tạo project trong kho lưu trữ riêng tư:

```text
pse new /duong-dan/toi/private-projects
```

Sau đó:

```text
pse build .
pse check . --human
pse proof . --recipient "Tên người nhận"
pse release .
pse verify-release release/<release-id>
```

Xem [Onboarding](docs/workflows/ONBOARDING.md) để đọc workflow đầy đủ. Với PDF hoàn chỉnh, xem [Output inspection and accessibility baseline](docs/getting-started/OUTPUT-INSPECTION-ACCESSIBILITY.md). Audit evidence có thể được kiểm bằng `pse verify-audit-record` / `pse verify-audit-index` và export reproducibly bằng `pse export-audit-evidence`; xem [Audit evidence verification and deterministic export](docs/release/AUDIT-EVIDENCE-VERIFICATION-AND-EXPORT.md).

## Ranh giới kiến trúc

- **Core** cung cấp hạ tầng production dùng chung.
- **Profile** cung cấp presentation và page architecture.
- **Semantic module** cung cấp cấu trúc có nghĩa và contract QA.
- **Title project** cung cấp nội dung chuẩn, metadata và cấu hình riêng.
- **Security, QA, runtime, proof và release provenance** luôn thuộc backbone, không được duplicate trong profile/module.

Xem [Architecture Specification](docs/architecture/ARCHITECTURE-SPECIFICATION.md), [Profile API](docs/architecture/PROFILE-API-CONTRACT.md) và [Semantic Module Architecture](docs/architecture/SEMANTIC-MODULE-ARCHITECTURE.md).

## Mô hình bảo mật

PSE được thiết kế để chạy trong infrastructure do nhà xuất bản kiểm soát. LuaLaTeX shell escape bị tắt theo mặc định; YAML và metadata bridge được validate; bản thảo chưa phát hành không cần rời khỏi môi trường của publisher. Watermark proof riêng theo người nhận là cơ chế **ngăn cản + truy nguyên**, không phải DRM không thể gỡ.

Không bao giờ đính kèm bản thảo chưa phát hành, recipient proof, secret hay dữ liệu production độc quyền vào public issue. Xem [Security](SECURITY.md) và `docs/security/`.

## Triết lý QA và phát hành

Machine finding có bốn mức:

- `error` — chặn;
- `warning` — cảnh báo kỹ thuật;
- `review` — cần phán đoán của editor/production staff;
- `info` — bằng chứng/trạng thái được ghi lại.

Build thành công không tự động là bản phát hành. Dùng `pse release` và `pse verify-release` để tạo và kiểm artifact phát hành chính thức.

## Giấy phép, trích dẫn và sử dụng thương mại

PSE hiện là **source-available trong giai đoạn phát triển**. Giấy phép công khai cuối cùng chưa được phát hành. Việc nhìn thấy source không tự động cấp quyền institutional, commercial, enterprise, embedding, OEM, white-label, hosted hoặc managed-service.

Mọi ebook được tạo qua publication-release pipeline của PSE phải có banner attribution chuẩn của PSE trên trang copyright/publication hoặc colophon. Trang publication mặc định tự chèn banner, và `pse release` sẽ chặn nếu final build không có bằng chứng banner đã được render. Banner chứa dòng attribution chuẩn:

> **Produced with Publication Systems Engineering.**

Đây hiện là release contract ở cấp framework; việc attribution có trở thành nghĩa vụ pháp lý của giấy phép hay không vẫn chờ independent legal review. Xem [Brand and Attribution](docs/design/BRAND-AND-ATTRIBUTION.md), [Licensing Overview](docs/licensing/OVERVIEW.md), [Commercial Licensing Inquiry](docs/licensing/COMMERCIAL-LICENSING-INQUIRY.md) và [`LICENSE-STATUS.md`](LICENSE-STATUS.md). Metadata trích dẫn nằm trong [`CITATION.cff`](CITATION.cff).

## Contract beta-candidate

Public command/schema surface đang được giữ ổn định trong khi hoàn tất legal review và release evidence. Xem:

- [Beta Candidate Freeze](docs/beta/BETA-CANDIDATE-FREEZE.md)
- [Public Beta Checklist](docs/beta/PUBLIC-BETA-CHECKLIST.md)
- [CLI Compatibility Matrix](docs/reference/CLI-COMPATIBILITY-MATRIX.md)
- [API & Schema Compatibility](docs/reference/API-SCHEMA-COMPATIBILITY.md)
- [Compatibility & Migration Policy](docs/architecture/COMPATIBILITY-MIGRATION-POLICY.md)
- [Support Matrix](docs/reference/SUPPORT-MATRIX.md)

## Đóng góp

PSE theo mô hình maintainer-led nhưng contribution-friendly. Tuy nhiên việc nhận external code contribution vẫn bị chặn cho tới khi contributor-rights/dual-licensing policy được khóa. Khi public repository được staging, bug report nhỏ có synthetic reproducer và proposal đúng architecture sẽ là hình thức đóng góp phù hợp nhất.

Xem [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Nguồn gốc dự án

Publication Systems Engineering là một đóng góp công khai được phát triển trong bối cảnh rộng hơn của dự án **Marginalia – Trật tự ẩn**. Repository này không chứa architecture riêng tư, title-specific source, production code hay tài liệu nội bộ của dự án đó.

## Maintainer

**Quoc-Tan Tran**


## Documentation

Public explanatory documentation is maintained from [`wiki/`](wiki/index.md). Technical contracts remain under [`docs/`](docs/).
