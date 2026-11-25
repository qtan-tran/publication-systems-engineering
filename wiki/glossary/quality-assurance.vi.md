---
title: Kiểm soát chất lượng và phát hành
description: Tóm lược quy trình Quality Assurance của PSE cùng các khái niệm về kiểm định, kiểm thử hồi quy, các lớp xác nhận chất lượng và quyết định phát hành.
---

# Kiểm soát chất lượng và phát hành

Một hệ thống xuất bản không chỉ cần tạo được một cuốn sách tốt, mà còn phải giúp bảo đảm những sửa đổi tiếp theo không phá hỏng các thành phần vốn đang hoạt động đúng. Nhóm thuật ngữ này là nền tảng của Quality Assurance trong PSE.

## Quy trình Quality Assurance của PSE (tóm lược)

Quy trình dưới đây tổng hợp các khái niệm trong trang này thành một luồng công việc; mô hình bốn lớp xác nhận cuối cùng là phần đề xuất rút ra từ kinh nghiệm của các dự án sản xuất thực tế.

1. **Chuẩn bị môi trường và khóa phạm vi.** Kiểm tra môi trường tạo lập bằng `pse doctor`; xác lập văn bản nền, [hệ định vị](locators-and-references.md) và phạm vi thay đổi قبل khi bắt đầu (khóa nguồn, khóa biên tập, khóa chế bản).
2. **Kiểm tra trước sản xuất.** Xác nhận tệp nguồn, tài nguyên, phông chữ và cấu hình đầy đủ trước khi tạo sách.
3. **Tạo lập ấn bản.** Chạy `pse build .`; quy trình biên dịch qua nhiều lượt để số trang, mục lục và tham chiếu ổn định; ưu tiên tạo lập sạch khi nghi ngờ tệp trung gian lỗi thời.
4. **Kiểm định cấu trúc.** Chạy `pse check . --human`: đối chiếu tập định vị, điểm neo, mục lục, chỉ mục, siêu dữ liệu và liên kết kỹ thuật; đọc kết quả theo bốn mức `error`, `warning`, `review`, `info` và xử lý hết lỗi mức `error` trước khi tiếp tục.
5. **Kiểm định hình ảnh và hình học.** Kết xuất trang thành hình ảnh, so sánh với mốc đối chiếu (so sánh hình ảnh trang), xem bảng ảnh thu nhỏ và kiểm tra vị trí dấu chỉ nằm đúng lề, đúng trang.
6. **Kiểm định đầu ra.** Chạy `pse inspect-output .` để ghi nhận đường cơ sở về siêu dữ liệu, điều hướng và khả năng trích xuất văn bản của PDF hoàn chỉnh.
7. **Kiểm định nội dung do con người.** Đọc soát toàn trang ở độ phân giải đầy đủ, đối soát ý nghĩa liên kết và sổ đối chiếu ngữ nghĩa; mọi phát hiện mức `review` cần phán đoán của người biên tập, không thể đóng bằng phép kiểm tra hình thức.
8. **Tổng hợp theo bốn lớp xác nhận.** (1) nguồn và văn bản nền, (2) nội dung và ngữ văn, (3) cấu trúc và tra cứu, (4) chế bản và sản xuất (chi tiết ở cuối trang).
9. **Quyết định phát hành.** Chốt các điều kiện hoàn tất, phân biệt vấn đề cản trở phát hành với vấn đề tồn đọng, rồi mới dùng `pse release .` và `pse verify-release` cho ranh giới phát hành.
10. **Kiểm thử hồi quy sau mọi thay đổi.** Với mỗi sửa đổi, chạy lại các kiểm định trên phần có liên quan; khi sửa phần dùng chung, kiểm thử hồi quy liên đầu sách cho mọi ấn bản dùng chung phần đó.

Các trang tiếng Anh trình bày sâu hơn từng khâu: [Quality Model](../quality-release/quality-model.md), [Build and check your PDF](../getting-started/build-and-check.md), và [Human Review](../workflows/human-review.md).

## Các nguyên tắc kiểm định

| Thuật ngữ | Giải thích |
| --- | --- |
| **Bảo đảm chất lượng** (quality assurance, QA) | Hệ thống nguyên tắc và quy trình được xây dựng để phòng ngừa, phát hiện và xử lý các vấn đề chất lượng trong toàn bộ quá trình sản xuất. |
| **Kiểm soát chất lượng** (quality control, QC) | Hoạt động kiểm tra các sản phẩm cụ thể để xác định chúng có đáp ứng tiêu chuẩn đã đặt ra hay không. |
| **Kiểm thử** (testing) | Thực hiện một phép kiểm tra có điều kiện và kết quả kỳ vọng xác định trước. |
| **Bộ kiểm định** (validator) | Công cụ hoặc tập hợp quy tắc dùng để xác nhận một thành phần có tuân thủ các yêu cầu đã xác lập hay không. |
| **Điều kiện đạt** (acceptance criteria) | Tiêu chí cụ thể để kết luận một sản phẩm hoặc công việc đáp ứng yêu cầu. |
| **Chốt kiểm định** (quality gate) | Điểm kiểm tra mà tại đó một số điều kiện phải được đáp ứng trước khi dự án chuyển sang trạng thái tiếp theo. |
| **Kiểm định độc lập** (independent validation) | Kiểm tra dựa trên nguồn, phương pháp hoặc người thẩm định đủ độc lập với công việc đã tạo ra sản phẩm cần kiểm định. |
| **Bằng chứng kiểm định** (validation evidence) | Kết quả đo, hồ sơ đối chiếu, hình ảnh, nhật ký hoặc nhận xét có thể sử dụng để hỗ trợ kết luận chất lượng. |
| **Phạm vi kiểm định** (validation coverage) | Phần nội dung, chức năng hoặc trường hợp thực tế đã được kiểm tra. |
| **Kiểm tra chọn mẫu** (spot check) | Kiểm tra một số trường hợp được lựa chọn thay vì toàn bộ đối tượng. Kết quả chỉ có giá trị trong phạm vi tương ứng. |

## Kiểm thử hồi quy

**Lỗi hồi quy** (regression) là lỗi phát sinh sau một thay đổi, làm cho một chức năng hoặc đặc tính từng hoạt động đúng trở nên sai hoặc không còn đáp ứng yêu cầu. **Kiểm thử hồi quy** (regression testing) là kiểm tra lại những chức năng đã được xác nhận trước đó sau khi thực hiện thay đổi, nhằm phát hiện các tác động ngoài dự kiến. Ví dụ, sửa lại cách trình bày chỉ mục có thể vô tình làm sai mục lục, thay đổi số trang hoặc ảnh hưởng đến cách trình bày của một cuốn sách khác sử dụng chung mẫu chế bản.

Kiểm thử hồi quy không yêu cầu mọi thứ phải giữ nguyên. Nó yêu cầu những thay đổi có chủ ý được thực hiện đúng và những thành phần không nằm trong phạm vi thay đổi vẫn hoạt động như mong đợi.

| Thuật ngữ | Giải thích |
| --- | --- |
| **Kiểm thử hồi quy liên đầu sách** (cross-title regression testing) | Kiểm tra nhiều đầu sách khác nhau sau khi sửa hệ thống lõi dùng chung, nhằm phát hiện tác động ngoài phạm vi dự án đang thực hiện. |
| **Mẫu kiểm thử** (test fixture) | Một tài liệu hoặc tập dữ liệu được chuẩn bị để kiểm tra một trường hợp xác định, chẳng hạn hai nhân vật cùng nói trong một câu thơ. |
| **Cô lập phạm vi thay đổi** (change isolation) | Giới hạn sửa đổi vào phần thực sự cần xử lý, nhằm giảm nguy cơ tạo ra lỗi tại những thành phần khác. |
| **Phạm vi ảnh hưởng** (blast radius) | Số lượng và mức độ các thành phần hoặc dự án có thể bị tác động bởi một thay đổi. |

Đối với PSE, việc sửa một quy tắc riêng của một đầu sách cụ thể có phạm vi ảnh hưởng khác với việc sửa quy tắc chung của toàn bộ tủ sách; hai loại thay đổi cần những mức độ kiểm định khác nhau.

## Kiểm định cấu trúc, vị trí và ý nghĩa

| Thuật ngữ | Giải thích |
| --- | --- |
| **Kiểm định cấu trúc** (structural QA) | Kiểm tra sự đầy đủ và tính hợp lệ của những thành phần như số trang, điểm neo, mục lục, chỉ mục, liên kết và siêu dữ liệu. |
| **Kiểm định ngữ nghĩa** (semantic QA) | Kiểm tra xem các nội dung và mối quan hệ trong tài liệu có đúng về ý nghĩa hay không. |
| **Kiểm định hình học** (geometry validation) | Kiểm tra vị trí, kích thước, khoảng cách và sự chồng lấn của các thành phần trên trang. |
| **Kiểm thử hồi quy vị trí dấu chỉ** (marker geometry regression) | Kiểm tra lại vị trí của các dấu chỉ sau khi sửa đổi, nhằm bảo đảm chúng vẫn nằm đúng lề, đúng trang, tương ứng với điểm neo và không chồng lên nội dung. |
| **Đối chiếu tập định vị** (locator-set validation) | So sánh tập định vị thực tế với tập định vị được kỳ vọng theo ấn bản nguồn để phát hiện thiếu, trùng hoặc sai thứ tự. |
| **Đối soát khai báo và sản phẩm** (claim-to-output validation) | Kiểm tra xem những gì người biên tập tuyên bố trong sách có phù hợp với nội dung và hình thức thực tế hay không. |

Vị trí chuẩn của dấu chỉ phụ thuộc vào quy tắc chế bản, đường chân chữ, khổ sách và hồ sơ trình bày; không nên dùng một khoảng cách cố định cho mọi loại ấn bản, và mọi dung sai phải được nêu rõ thay vì ngầm định.

## Kiểm tra hình ảnh và đọc soát trang

| Thuật ngữ | Giải thích |
| --- | --- |
| **Kết xuất hình ảnh trang** (rendering) | Chuyển một trang tài liệu thành hình ảnh có thể quan sát hoặc phân tích trực tiếp. |
| **So sánh hình ảnh trang** (render-diff) | Kết xuất cùng một trang hoặc nội dung từ hai phiên bản rồi so sánh để phát hiện những thay đổi thị giác. |
| **So sánh điểm ảnh** (pixel comparison) | Một phương pháp so sánh hình ảnh dựa trên sự khác biệt giữa từng điểm ảnh trong cùng điều kiện kết xuất. |
| **Trang giống hệt về điểm ảnh** (pixel-identical page) | Trang có hình ảnh kết xuất giống hệt trang tham chiếu trong điều kiện so sánh xác định. Không nhất thiết có nghĩa mọi dữ liệu bên trong PDF đều giống nhau. |
| **Bảng ảnh thu nhỏ** (contact sheet) | Tập hợp nhiều trang dưới dạng ảnh thu nhỏ để quan sát tổng thể nhịp điệu, bố cục và tính nhất quán của sách. |
| **Đọc soát toàn trang** (page-by-page proofing) | Kiểm tra lần lượt các trang của ấn bản nhằm phát hiện vấn đề nội dung, bố cục và trải nghiệm đọc. |
| **Danh sách đọc soát ở độ phân giải đầy đủ** (full-resolution proof queue) | Danh sách những trang cần được kiểm tra chi tiết ở kích thước và chất lượng đủ để đọc rõ chữ, dấu và các thành phần nhỏ. |
| **Sai khác ngoài dự kiến** (unexpected diff) | Thay đổi giữa hai phiên bản không nằm trong phạm vi sửa đổi được chủ định hoặc chưa có lý do giải thích. |

### Phân biệt so sánh hình ảnh và so sánh nội dung

So sánh hình ảnh giúp xác định **nơi** có thay đổi; người kiểm định vẫn cần đọc và đánh giá xem thay đổi đó là sửa chữa đúng, lỗi mới hay một khác biệt không đáng kể.

Trong bản đọc soát biên tập cuối của một dự án sản xuất thực tế, hồ sơ ghi nhận 80 trong tổng số 94 trang giống hệt về điểm ảnh so với bản thử chế bản ở độ phân giải 72 dpi, còn 14 trang có thay đổi. Kết quả so sánh ở 72 dpi không thay thế việc đọc soát toàn bộ sách ở độ phân giải đầy đủ. Điều quan trọng không phải là đạt tỷ lệ trang giống hệt cao nhất, mà là có thể **giải thích được** những thay đổi đã xảy ra và kiểm định được tác động của chúng.

## Xác nhận chất lượng và phát hành

| Thuật ngữ | Giải thích |
| --- | --- |
| **Bản thảo biên tập** (editorial draft) | Phiên bản đang được hoàn thiện về nội dung, cấu trúc, chú thích và các quyết định biên tập. |
| **Bản thử chế bản** (production proof) | Phiên bản đã được tạo lập thành hình thức sách để kiểm tra bố cục, chữ, phân trang và các đặc tính kỹ thuật. |
| **Bản đọc soát biên tập cuối** (final editorial proof) | Phiên bản được chuẩn bị cho việc đọc soát và thẩm định biên tập cuối cùng. Tên gọi này không mặc nhiên có nghĩa mọi kiểm định đã hoàn tất. |
| **Khóa biên tập** (editorial freeze) | Xác lập trạng thái ổn định của nội dung và các quyết định biên tập để tiến hành những bước kiểm tra tiếp theo. |
| **Khóa chế bản** (production freeze) | Xác lập trạng thái ổn định của bố cục và quy trình sản xuất, hạn chế những thay đổi ngoài phạm vi đã xác định. |
| **Xác nhận hoàn tất** (sign-off) | Quyết định có căn cứ rằng một phạm vi công việc đã đáp ứng các điều kiện đặt ra và có thể được coi là hoàn thành. |
| **Điều kiện hoàn tất** (definition of done) | Tập hợp yêu cầu xác định trước mà một công việc, giai đoạn hoặc ấn bản cần đáp ứng để được coi là hoàn thành. |
| **Vấn đề cản trở phát hành** (release blocker) | Vấn đề đủ nghiêm trọng để một ấn bản chưa thể được phát hành, chẳng hạn nội dung bị bỏ sót, tệp sách hư hỏng hoặc quyền sử dụng nguồn chưa được xác nhận. |
| **Vấn đề tồn đọng** (known issue) | Vấn đề đã được nhận diện và ghi nhận nhưng chưa được xử lý hoàn toàn. Tùy mức độ, nó có thể cản trở hoặc không cản trở phát hành. |
| **Bản phát hành chính thức** (release) | Phiên bản được xác nhận đáp ứng các điều kiện xuất bản và được đưa đến độc giả theo phạm vi đã xác định. |
| **Báo cáo tổng kết kỹ thuật** (technical postmortem) | Tài liệu phân tích những vấn đề đã xảy ra trong quá trình sản xuất, nguyên nhân, cách xử lý, giới hạn kiểm chứng và bài học có thể áp dụng cho các dự án tiếp theo. |

### Bốn lớp xác nhận chất lượng của một ấn bản

Từ kinh nghiệm sản xuất thực tế, mô hình đề xuất cho PSE là phân biệt **bốn lớp xác nhận** thay vì dùng một kết luận chung rằng cuốn sách đã hoàn thành:

1. **Xác nhận nguồn và văn bản nền.** Đúng nguồn, đúng ấn bản, đúng quy ước định vị; quyền sử dụng và lai lịch nguồn được làm rõ.
2. **Xác nhận nội dung và ngữ văn.** Bản dịch, phân vai, diễn giải và các quyết định biên tập có căn cứ thích hợp.
3. **Xác nhận cấu trúc và tra cứu.** Các phần nội dung, chú thích, chỉ mục và liên kết tương ứng đúng với nhau.
4. **Xác nhận chế bản và sản xuất.** Bố cục, tệp sách, phông chữ, quy trình tạo lập và gói lưu trữ đáp ứng yêu cầu.

Quyết định phát hành được đưa ra dựa trên bằng chứng của cả bốn lớp. Việc tách nguồn và ngữ văn thành hai lớp riêng đúng với nguyên tắc không dùng một loại bằng chứng để chứng minh một loại chất lượng khác: kiểm định cấu trúc kỹ thuật không thay thế được [xác nhận ngữ văn](textual-scholarship.md).

Bảng thuật ngữ liên quan: [Tạo lập ấn bản và phiên bản](build-and-versioning.md), tổng quan ở [Bảng thuật ngữ PSE](index.md).
