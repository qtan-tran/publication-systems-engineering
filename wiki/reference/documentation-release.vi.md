# Bằng chứng phát hành tài liệu

Website tài liệu công khai được sinh ra từ các tệp Markdown trong `/wiki`. Website được sinh là một sản phẩm tạo lập của quy trình tài liệu; nó không phải một nguồn chỉnh sửa bổ sung.

Với các bản tạo lập triển khai, PSE kiểm định nguồn, tạo lập site ở chế độ strict, so sánh siêu dữ liệu HTML sinh ra và sitemap với URL cơ sở triển khai thực tế, và tạo một bảng kê tệp SHA-256 tên `documentation-release-evidence.json`. Bản ghi bằng chứng gắn các tệp được sinh với một phiên bản PSE và một bản sửa đổi nguồn.

Bản ghi này cố tình hẹp. Nó không tuyên bố một bản triển khai đang chạy, và nó không phải một chữ ký số, dấu thời gian tin cậy, chứng thực hay chứng nhận bảo tồn.

Các đường dẫn tài liệu đã phát hành được theo dõi đối chiếu một đường cơ sở URL ổn định. Một đường dẫn đã phát hành trước đó không nên biến mất im lặng; thay đổi đường dẫn cần một quyết định chuyển hướng hay di dời tường minh.

PSE hiện không phát hành một bản sao GitHub Wiki. `/wiki` vẫn là nguồn chuẩn, và MkDocs Pages vẫn là sản phẩm tài liệu được kết xuất chính.
