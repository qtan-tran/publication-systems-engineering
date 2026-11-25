---
title: Tạo lập ấn bản và phiên bản
description: Quy trình tạo lập, quản lý phiên bản, đóng gói, lưu trữ và siêu dữ liệu của ấn bản trong PSE.
---

# Tạo lập ấn bản và phiên bản

Nhóm này giúp phân biệt giữa việc tạo ra một tệp sách và việc xây dựng một hệ thống có khả năng sản xuất, bảo trì và tái bản sách một cách bền vững.

## Quy trình tạo lập ấn bản

| Thuật ngữ | Giải thích |
| --- | --- |
| **Tệp nguồn** (source file) | Tệp chứa nội dung, cấu trúc hoặc quy tắc thiết kế được sử dụng để tạo ra ấn bản. Đây là nơi nên thực hiện các chỉnh sửa lâu dài. |
| **Tài nguyên xuất bản** (asset) | Những thành phần hỗ trợ việc tạo sách như hình ảnh, bản đồ, logo, bìa hoặc phông chữ được phép sử dụng. |
| **Tạo lập ấn bản** (build) | Quá trình sử dụng tệp nguồn, tài nguyên và các công cụ chế bản để tạo ra sản phẩm có thể đọc được, chẳng hạn PDF hoặc EPUB. |
| **Quy trình tạo lập** (build pipeline) | Chuỗi công việc có tổ chức để kiểm tra đầu vào, tạo sách, xây dựng mục lục và chỉ mục, kiểm định và đóng gói sản phẩm. |
| **Kiểm tra trước sản xuất** (preflight) | Kiểm tra các điều kiện cần thiết trước khi tạo sách, chẳng hạn tệp nguồn có đầy đủ không, phông chữ có sẵn không và cấu hình có phù hợp không. |
| **Lượt biên dịch** (compilation pass) | Một lần công cụ chế bản xử lý tài liệu. Có thể cần nhiều lượt để số trang, mục lục và các tham chiếu ổn định. |
| **Tệp trung gian** (auxiliary file) | Tệp được sinh ra trong quá trình chế bản để lưu thông tin tạm thời, chẳng hạn số trang hoặc dữ liệu tham chiếu. |
| **Tạo lập sạch** (clean build) | Tạo lại ấn bản mà không phụ thuộc vào những tệp trung gian cũ có khả năng chứa dữ liệu lỗi thời hoặc hư hỏng. |
| **Tạo lập có thể tiếp tục** (resumable build) | Quy trình có thể tiếp tục từ một bước đã được xác nhận hợp lệ sau khi bị gián đoạn, thay vì phải thực hiện lại mọi công việc từ đầu. |
| **Môi trường tạo lập** (build environment) | Tập hợp phần mềm, phiên bản công cụ, phông chữ, cấu hình và điều kiện cần thiết để tạo ra ấn bản. |
| **Khả năng tái tạo** (reproducibility) | Khả năng tạo lại ấn bản từ những nguồn và điều kiện đã được lưu trữ, với mức độ tương đồng được xác định trước. |

### Tại sao một cuốn sách cần được tạo lập nhiều lượt?

Muốn tạo một chỉ mục chính xác, hệ thống cần biết mỗi thuật ngữ xuất hiện trên trang nào. Nhưng việc bổ sung chỉ mục hoặc cập nhật mục lục có thể tiếp tục ảnh hưởng đến cách phân trang. Vì thế, tạo lập sách là một quá trình có sự phụ thuộc giữa các bước: lượt đầu dàn trang xác định nội dung nằm trên những trang nào; sau đó tập hợp mục từ, số trang và tham chiếu để tạo thông tin tra cứu; các lượt tiếp theo đưa thông tin tra cứu vào sách và tính lại phân trang; cuối cùng kiểm tra số trang và tham chiếu không còn thay đổi ngoài dự kiến. Nó không nhất thiết là một lần chuyển đổi từ văn bản sang PDF.

## Phiên bản và mốc đối chiếu

| Thuật ngữ | Giải thích |
| --- | --- |
| **Phiên bản** (version) | Một trạng thái được xác định của nội dung, mã nguồn hoặc ấn bản tại một thời điểm. |
| **Mốc đối chiếu** (baseline) | Phiên bản được lựa chọn làm căn cứ để so sánh và đánh giá những thay đổi tiếp theo. Không nhất thiết là phiên bản mới nhất. |
| **Bản chụp trạng thái** (snapshot) | Bản lưu giữ tình trạng của một dự án tại một thời điểm, giúp kiểm tra hoặc khôi phục trạng thái đó. |
| **Bản sửa đổi** (patch) | Một tập hợp thay đổi nhằm xử lý một vấn đề hoặc nhóm vấn đề cụ thể. |
| **Nhật ký thay đổi** (changelog) | Hồ sơ ghi lại những thay đổi có ý nghĩa giữa các phiên bản và lý do thực hiện. |
| **Bản ứng viên phát hành** (release candidate) | Phiên bản được chuẩn bị để kiểm định trước khi có thể trở thành bản phát hành chính thức. |
| **Khóa trạng thái** (freeze) | Tạm thời ngừng thay đổi một phạm vi đã xác định để tạo điều kiện kiểm định và tránh phát sinh những sửa đổi không cần thiết. |
| **Khôi phục phiên bản** (rollback) | Quay lại một trạng thái đã được lưu trữ khi phiên bản mới phát sinh vấn đề nghiêm trọng hoặc không đáp ứng tiêu chuẩn. |
| **Ghi chú tiếp nối** (continuation note) | Tài liệu ngắn ghi nhận trạng thái hiện tại, công việc đã hoàn thành, vấn đề còn mở và điểm bắt đầu cho giai đoạn tiếp theo. |

Mốc đối chiếu có vai trò đặc biệt quan trọng: không thể đánh giá một thay đổi là cải tiến hay sai sót mới nếu không xác định rõ đang so sánh với trạng thái nào.

## Đóng gói và lưu trữ

| Thuật ngữ | Giải thích |
| --- | --- |
| **Sản phẩm tạo lập** (artifact) | Tệp hoặc sản phẩm cụ thể được sinh ra trong quy trình, chẳng hạn PDF, báo cáo kiểm định, bản đồ hoặc gói mã nguồn. |
| **Gói dự án** (project bundle) | Tập hợp tệp nguồn, tài nguyên, cấu hình và tài liệu cần thiết được đóng gói thành một đơn vị có thể lưu trữ hoặc chuyển giao. |
| **Gói công khai** (public bundle) | Gói tài liệu được chuẩn bị để chia sẻ công khai, chỉ bao gồm những thành phần phù hợp về quyền sử dụng, bảo mật và phạm vi phát hành. |
| **Gói hạn chế truy cập** (confidential bundle) | Gói tài liệu chứa thông tin, tài nguyên hoặc hồ sơ nội bộ không được công bố công khai. Việc gọi một gói là hạn chế truy cập không tự động bảo đảm nó được bảo mật; cần có cơ chế quản lý thích hợp. |
| **Gói lưu trữ** (archival bundle) | Gói được giữ lại để bảo tồn hồ sơ sản xuất, phục vụ kiểm định, khôi phục hoặc tái bản trong tương lai. |
| **Gói phát hành** (release bundle) | Tập hợp các sản phẩm được chuẩn bị cho mục đích phát hành, không nhất thiết chứa toàn bộ lịch sử và tài liệu nội bộ của dự án. |
| **Bảng kê sản phẩm** (artifact manifest) | Danh sách có cấu trúc ghi nhận các tệp trong một gói, cùng thông tin cần thiết như tên, phiên bản, vai trò hoặc mã kiểm toàn vẹn. |
| **Mã kiểm toàn vẹn** (checksum) | Giá trị được tính từ dữ liệu của tệp để phát hiện tệp đã thay đổi hoặc hư hỏng so với bản tham chiếu hay chưa. |
| **Kiểm tra tính toàn vẹn** (integrity check) | Xác minh tệp hoặc gói tài liệu không bị thiếu, lỗi hoặc thay đổi ngoài dự kiến. |
| **Khả năng bảo trì** (maintainability) | Mức độ dễ dàng và an toàn khi sửa chữa, cập nhật hoặc tiếp tục phát triển một hệ thống xuất bản. |

Một gói dự án đầy đủ gồm: nội dung nguồn (bản dịch, khảo chú, thư mục), tài nguyên (bìa, bản đồ, hình ảnh được phép sử dụng), cấu hình chế bản, ấn bản PDF, báo cáo kiểm định, bảng kê sản phẩm kèm mã kiểm toàn vẹn và ghi chú tiếp nối.

Trong một dự án sản xuất thực tế, đã có thời điểm thư mục làm việc không còn đầy đủ tệp nguồn và dự án phải được khôi phục từ một gói lưu trữ trước đó. Kinh nghiệm này cho thấy thư mục đang làm việc không thể thay thế cho một hồ sơ lưu trữ bền vững. Một cuốn sách chỉ tồn tại dưới dạng PDF có thể vẫn đọc được, nhưng khả năng sửa chữa và tái bản về sau sẽ bị giới hạn nếu không còn nguồn sản xuất.

## Siêu dữ liệu và đặc tính kỹ thuật của sách điện tử

Siêu dữ liệu thường không xuất hiện trực tiếp trên trang sách nhưng có vai trò quan trọng đối với việc nhận diện, quản lý, tìm kiếm và lưu trữ ấn bản.

| Thuật ngữ | Giải thích |
| --- | --- |
| **Siêu dữ liệu** (metadata) | Dữ liệu mô tả một tài liệu, chẳng hạn tên sách, tác giả, dịch giả, ngôn ngữ, ngày xuất bản, quyền sử dụng và phiên bản. |
| **Chuẩn siêu dữ liệu mở rộng** (XMP, Extensible Metadata Platform) | Một khuôn khổ tiêu chuẩn cho phép lưu trữ siêu dữ liệu có cấu trúc bên trong tài liệu, bao gồm PDF. |
| **Khai báo ngôn ngữ tài liệu** (document language) | Thông tin xác định ngôn ngữ chính của tài liệu, giúp phần mềm đọc và xử lý văn bản phù hợp hơn. |
| **Định danh bền vững** (persistent identifier) | Định danh được thiết kế để duy trì khả năng nhận diện một tài liệu trong thời gian dài, chẳng hạn DOI hoặc ISBN với các chức năng khác nhau. |
| **Tài nguyên phông chữ** (font resource) | Dữ liệu liên quan đến phông chữ được tài liệu sử dụng hoặc khai báo. Một tài nguyên được liệt kê không nhất thiết thực sự xuất hiện trong nội dung hiển thị. |
| **Khả năng trích xuất văn bản** (text extractability) | Khả năng lấy nội dung chữ từ tài liệu điện tử để tìm kiếm, sao chép hoặc xử lý bằng công cụ khác. |
| **Khả năng tiếp cận** (accessibility) | Mức độ tài liệu có thể được sử dụng bởi những người có nhu cầu tiếp cận khác nhau, bao gồm người sử dụng trình đọc màn hình hoặc công nghệ hỗ trợ. |
| **PDF lưu trữ** (PDF/A) | Họ tiêu chuẩn PDF được thiết kế cho mục đích lưu trữ tài liệu lâu dài. |
| **PDF hỗ trợ tiếp cận** (PDF/UA) | Họ tiêu chuẩn quy định các yêu cầu kỹ thuật đối với khả năng tiếp cận của tài liệu PDF. |

XMP khác với thông tin được in trên sách: cùng một ấn bản có một lớp thông tin người đọc nhìn thấy trên trang bìa và trang tựa, và một lớp thông tin phần mềm đọc được như tên tài liệu, tác giả, ngôn ngữ, trạng thái. Việc có siêu dữ liệu XMP, khai báo ngôn ngữ và nhúng phông chữ đầy đủ là những đặc tính kỹ thuật hữu ích, nhưng chúng không tự động chứng minh tài liệu đã đáp ứng toàn bộ tiêu chuẩn PDF/A hay PDF/UA; các tiêu chuẩn ấy có những yêu cầu kiểm định riêng.

Bảng thuật ngữ liên quan: [Kiểm soát chất lượng và phát hành](quality-assurance.md), [Thiết kế chữ và chế bản](typography-and-layout.md).
