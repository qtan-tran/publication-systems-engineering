---
title: Bảng thuật ngữ PSE
description: Bảng thuật ngữ khái niệm về kiến trúc ấn bản, biên tập, chế bản và kiểm soát chất lượng của Publication Systems Engineering, viết bằng tiếng Việt.
---

# Bảng thuật ngữ PSE

Bảng thuật ngữ này trình bày các khái niệm của Publication Systems Engineering (PSE) theo **kiến trúc khái niệm của một hệ thống xuất bản**, chứ không theo thứ tự từ A đến Z. Cách tổ chức này giúp người chưa có kiến thức về lập trình, LaTeX hay thiết kế sách hiểu được các thuật ngữ trong mối quan hệ với nhau, đồng thời hiểu tại sao chúng cần thiết trong quy trình làm sách.

Các định nghĩa lấy kinh nghiệm của các dự án sản xuất ấn bản thực tế làm điểm xuất phát, nhưng được khái quát hóa để dùng cho nhiều loại hình xuất bản khác: sách chuyên khảo, giáo trình, tác phẩm triết học, kịch và ấn bản khảo chú học thuật.

Ưu tiên thuật ngữ tiếng Việt có nghĩa rõ ràng, dễ sử dụng lâu dài. Thuật ngữ tiếng Anh được giữ trong ngoặc ở lần xuất hiện đầu tiên để thuận tiện đối chiếu với mã nguồn và tài liệu kỹ thuật của PSE.

## Cấu trúc bảng thuật ngữ

- [Nguồn văn bản và kiểm định ngữ văn](textual-scholarship.md): đang chuyển tải văn bản nào đến người đọc, và dựa vào đâu để xác nhận đã chuyển tải đúng văn bản ấy.
- [Cấu trúc logic của văn bản](semantic-structure.md): văn bản được tổ chức như thế nào, độc lập với việc trình bày trên trang sách.
- [Hệ thống định vị và tra cứu](locators-and-references.md): định danh, điểm neo, mục lục, chỉ mục và các mối quan hệ tham chiếu giữa các phần nội dung.
- [Thiết kế chữ và chế bản](typography-and-layout.md): nội dung được chuyển thành hình thức có thể đọc được ra sao, đồng thời bảo đảm bản sắc thiết kế của từng ấn bản.
- [Tạo lập ấn bản và phiên bản](build-and-versioning.md): quy trình tạo lập, quản lý phiên bản, đóng gói, lưu trữ và siêu dữ liệu.
- [Kiểm soát chất lượng và phát hành](quality-assurance.md): kiểm định, kiểm thử hồi quy, các lớp xác nhận chất lượng và quyết định phát hành.

Đây là các nhóm khái niệm, không phải bảy công đoạn tuyến tính bắt buộc. Các lớp có quan hệ phụ thuộc và có thể được kiểm tra nhiều lần trong quá trình sản xuất.

Nguyên tắc nền tảng của PSE là **tách biệt nội dung, cấu trúc logic, hình thức trình bày và quy trình sản xuất, nhưng bảo đảm chúng luôn tương ứng với nhau**.

## Định nghĩa khái quát về PSE

**Publication Systems Engineering: Kỹ nghệ hệ thống xuất bản**

Kỹ nghệ hệ thống xuất bản là cách tiếp cận việc làm sách như một quá trình thiết kế, tổ chức, kiểm định và duy trì một hệ thống sản xuất ấn bản, thay vì chỉ như một công việc trình bày văn bản trên trang.

Hệ thống ấy bao gồm văn bản nguồn, cấu trúc nội dung, các quy ước định vị và tham chiếu, nguyên tắc thiết kế, công cụ chế bản, quy trình kiểm soát chất lượng và cơ chế lưu trữ, tái tạo ấn bản.

PSE hướng đến việc tách biệt những thành phần có chức năng khác nhau nhưng bảo đảm sự tương ứng giữa chúng; tiêu chuẩn hóa những công việc có thể tái sử dụng nhưng bảo toàn đặc điểm riêng của từng tác phẩm; tự động hóa những thao tác có quy tắc rõ ràng nhưng không thay thế phán đoán học thuật và biên tập bằng các phép kiểm tra hình thức.

Mục tiêu của PSE không chỉ là tạo ra những cuốn sách đẹp và nhất quán, mà còn là xây dựng một quy trình xuất bản có thể kiểm chứng, truy nguyên, sửa chữa, tái tạo và duy trì lâu dài.

## Những cặp khái niệm cần đặc biệt phân biệt

Các cặp dưới đây dễ bị nhầm lẫn trong trao đổi hằng ngày; phân biệt chúng rõ ràng giúp trao đổi về chất lượng sách chính xác hơn.

| Khái niệm A | Khái niệm B | Khác biệt cốt lõi |
| --- | --- | --- |
| Câu thơ | Dòng chữ vật lý | Đơn vị của tác phẩm và đơn vị trình bày trên trang. |
| Định vị chuẩn | Số trang | Vị trí theo quy ước văn bản và vị trí trong một ấn bản cụ thể. |
| Điểm neo | Dấu chỉ | Địa chỉ kỹ thuật và ký hiệu người đọc nhìn thấy. |
| Mục lục | Chỉ mục | Bản đồ cấu trúc cuốn sách và bản đồ các đối tượng nội dung. |
| Bảng thuật ngữ | Chỉ mục | Giải thích ý nghĩa và chỉ dẫn nơi xuất hiện. |
| Khóa chỉ mục | Mục từ hiển thị | Định danh quản lý và hình thức xuất hiện trước người đọc. |
| Liên kết hoạt động | Liên kết đúng nghĩa | Đích có thể truy cập và đích đúng với nội dung cần tham chiếu. |
| Bỏ sót | Khoảng khuyết | Lỗi trong quá trình biên tập và phần văn bản không còn được truyền lại đầy đủ. |
| Dị bản | Lỗi văn bản | Cách đọc khác có căn cứ và sai sót cần sửa chữa. |
| Kiểu trang | Hồ sơ trình bày | Quy tắc của một loại trang và hệ thống trình bày của một loại ấn bản. |
| Mốc đối chiếu | Phiên bản mới nhất | Căn cứ so sánh và trạng thái gần nhất. |
| Tạo lập thành công | Kiểm định thành công | Sản phẩm được tạo ra và sản phẩm đáp ứng yêu cầu kiểm tra. |
| Bảo đảm chất lượng | Kiểm soát chất lượng | Xây dựng hệ thống phòng ngừa lỗi và kiểm tra sản phẩm cụ thể. |
| Kiểm thử hồi quy | So sánh phiên bản | Kiểm tra sự bảo toàn chức năng và nhận diện những thay đổi. |
| Giống nhau về hình ảnh | Giống nhau về nội dung | Hình thức hiển thị tương đồng và nội dung, dữ liệu thực sự tương đồng. |
| Tính nhất quán | Tính đồng nhất | Chung nguyên tắc và giống nhau về hình thức. |
| Khóa trạng thái | Xác nhận hoàn tất | Tạm ngừng sửa đổi và xác nhận chất lượng có căn cứ. |
| Bản đọc soát cuối | Bản phát hành | Đối tượng cần thẩm định cuối cùng và sản phẩm được phép xuất bản. |
| Tệp sách | Gói dự án | Sản phẩm để đọc và hệ thống tài liệu để sản xuất, sửa chữa, tái bản. |

## Mười nguyên tắc nền tảng

### 1. Tách nội dung khỏi hình thức trình bày

Nội dung cần được nhận diện theo chức năng trước khi quyết định cách trình bày. Một tiêu đề là tiêu đề vì vai trò của nó trong văn bản, không phải vì nó được in chữ lớn. Nguyên tắc này tạo điều kiện thay đổi thiết kế, khổ sách hoặc định dạng mà không phải tổ chức lại toàn bộ nội dung.

### 2. Bảo toàn định danh của nội dung

Một đơn vị nguồn cần giữ được định danh trong phạm vi hệ định vị đã xác lập, dù vị trí của nó trong cuốn sách thay đổi. Đây là nền tảng của khả năng tra cứu, tham chiếu, đối chiếu và hiệu đính học thuật.

### 3. Kiểm tra các mối quan hệ, không chỉ từng thành phần

Một chú thích có thể đúng về nội dung nhưng được đặt sai vị trí. Một chỉ mục có thể được sắp xếp đẹp nhưng dẫn đến những trang không liên quan. Chất lượng của cuốn sách phụ thuộc cả vào chất lượng của từng bộ phận lẫn sự tương ứng giữa chúng.

### 4. Thực hiện sửa đổi tại nguồn

Nếu một mục từ bị trùng, nên sửa cách quản lý mục từ trong nguồn thay vì chỉ xóa mục trùng khỏi trang chỉ mục cuối cùng. Nếu mục lục ghi sai số trang, nên sửa cơ chế tạo mục lục thay vì gõ lại số trang bằng tay. Cách làm này xử lý nguyên nhân thay vì che đi biểu hiện của lỗi.

### 5. Tiêu chuẩn hóa chức năng, không áp đặt hình thức

Những thành phần cùng chức năng nên được quản lý bằng các nguyên tắc chung. Tuy nhiên, một vở kịch, một tác phẩm triết học và một giáo trình có thể cần những cách trình bày khác nhau. Một hệ thống xuất bản có khả năng mở rộng cần biết phần nào nên dùng chung và phần nào phải được thiết kế riêng.

### 6. Mọi thay đổi cần có phạm vi và căn cứ

Không phải mọi cải tiến của một cuốn sách đều nên được đưa vào hệ thống lõi. Một điều chỉnh riêng đầu sách có thể chỉ phục vụ một nhu cầu đặc thù. Chỉ nên đưa thay đổi vào phần dùng chung khi chức năng của nó đủ rõ, có giá trị tái sử dụng và đã được kiểm thử ở các loại ấn bản liên quan.

### 7. Không sử dụng một loại bằng chứng để chứng minh một loại chất lượng khác

Việc có đủ số dòng không chứng minh bản dịch đúng. Việc PDF mở được không chứng minh mọi liên kết đúng nghĩa. Việc phông chữ được nhúng không chứng minh tài liệu hoàn toàn dễ tiếp cận. Mỗi tuyên bố chất lượng cần được hỗ trợ bằng loại bằng chứng thích hợp.

### 8. Khả năng sửa chữa là một phần của chất lượng

Một hệ thống xuất bản tốt không chỉ tạo ra sản phẩm cuối cùng. Nó phải cho phép truy nguyên vấn đề, sửa đổi đúng phạm vi, khôi phục phiên bản và tạo lại sản phẩm mà không phát sinh chi phí không cần thiết.

### 9. Phân biệt bất định với sai sót

Trong xuất bản học thuật, không phải mọi bất định đều có thể được giải quyết. Một số vấn đề liên quan đến dị bản, lịch sử truyền bản hoặc diễn giải có thể tiếp tục tồn tại. Trách nhiệm của người biên tập là nhận diện, giải thích và ghi nhận trung thực những bất định đó, thay vì làm cho văn bản có vẻ chắc chắn một cách giả tạo.

### 10. Chất lượng phải tương xứng với chi phí kiểm định

Quy trình kiểm định không nên trở thành một hệ thống thủ tục cồng kềnh. Những việc lặp lại và có quy tắc rõ ràng nên được tự động hóa. Những việc đòi hỏi phán đoán ngữ văn, học thuật hoặc thẩm mỹ cần được dành công sức thích hợp. Mục tiêu không phải có nhiều bước kiểm tra nhất, mà là có đủ bằng chứng đáng tin cậy với một quy trình tinh gọn, bền vững và có khả năng mở rộng.

## Quy ước Việt hóa thuật ngữ

Để bảng thuật ngữ duy trì được lâu dài, cần thống nhất một số cách dịch chủ chốt ngay từ đầu.

| Tiếng Anh | Tiếng Việt |
| --- | --- |
| Publication Systems Engineering | Kỹ nghệ hệ thống xuất bản |
| Semantic structure | Cấu trúc logic của nội dung |
| Canonical locator | Định vị chuẩn |
| Anchor | Điểm neo |
| Marker | Dấu chỉ vị trí |
| Semantic edge | Quan hệ tham chiếu |
| Semantic alignment ledger | Sổ đối chiếu ngữ nghĩa |
| Normalization | Chuẩn hóa |
| Baseline | Mốc đối chiếu |
| Regression testing | Kiểm thử hồi quy |
| Render-diff | So sánh hình ảnh trang |
| Validator | Bộ kiểm định |
| Build | Tạo lập ấn bản |
| Resumable build | Tạo lập có thể tiếp tục |
| Artifact | Sản phẩm tạo lập |
| Manifest | Bảng kê |
| Checksum | Mã kiểm toàn vẹn |
| Freeze | Khóa trạng thái |
| Sign-off | Xác nhận hoàn tất |
| Proof | Bản đọc soát |
| Release | Phát hành |
| Definition of done | Điều kiện hoàn tất |
| Postmortem | Báo cáo tổng kết kỹ thuật |

Một số cách dịch như *kiểm thử hồi quy*, *siêu dữ liệu* và *chế bản* đã tương đối quen thuộc trong các lĩnh vực chuyên môn. Một số khác như *mốc đối chiếu*, *dấu chỉ vị trí*, *sổ đối chiếu ngữ nghĩa* và *tạo lập ấn bản* là lựa chọn Việt hóa được đề xuất riêng cho tài liệu PSE, nhằm cân bằng giữa tính chính xác và khả năng tiếp cận.

Không nhất thiết phải Việt hóa mọi tên riêng hoặc tên tiêu chuẩn. PSE, PDF, EPUB, XMP, Unicode và LaTeX vẫn nên được giữ nguyên.

## Phạm vi của bảng thuật ngữ

Bảng thuật ngữ này là bản đề xuất chuẩn hóa khái niệm, dựa trên các báo cáo tổng kết kỹ thuật của những dự án sản xuất thực tế và định hướng phát triển PSE, có bổ sung một số khái niệm tổng quát về xuất bản và kỹ nghệ phần mềm để tạo thành hệ thống nhất quán.

Nó chưa phải tài liệu đặc tả những chức năng hiện có trong mã nguồn PSE. Những cơ chế như mô hình định vị chuẩn dùng chung, bộ kiểm định theo từng hệ định vị, đối soát ý nghĩa liên kết hay tạo lập có thể tiếp tục cần được đối chiếu với tình trạng triển khai thực tế, trước khi tài liệu mô tả chúng như các tính năng đã hoàn thiện.

Về lâu dài, giá trị của bảng thuật ngữ không chỉ nằm ở việc giải thích các thuật ngữ kỹ thuật. Nó có thể trở thành nền tảng khái niệm chung của PSE, giúp tác giả, dịch giả, biên tập viên, nhà thiết kế và nhà phát triển phần mềm có cùng một ngôn ngữ khi trao đổi về cách một cuốn sách được tạo ra và điều gì làm cho cuốn sách ấy đáng tin cậy.
