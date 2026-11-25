---
title: Đọc soát bởi con người
description: Tách các phát hiện máy khỏi các quyết định biên tập, thiết kế chữ, sự thật và xuất bản cần con người.
---

# Đọc soát bởi con người

QA máy của PSE cố tình giới hạn. Nó phát hiện được nhiều vấn đề cấu trúc và kỹ thuật, nhưng không thể quyết định một bản dịch có chính xác không, một hệ khảo chú có đầy đủ về trí tuệ không, một thư mục có đúng về sự thật không, một điểm ngắt dòng có chấp nhận được về thẩm mỹ không, hay một trang đã sẵn sàng để một biên tập viên xác nhận hoàn tất chưa.

## Soát các phát hiện, rồi soát cuốn sách

Sau:

```text
pse check . --human
```

hãy lần lượt xử lý các cấp độ nghiêm trọng được báo:

| Cấp | Nghĩa sản xuất |
| --- | --- |
| `error` | điều kiện cản trở; sửa trước khi phát hành |
| `warning` | vấn đề kỹ thuật cần được chú ý |
| `review` | cần phán đoán tường minh của con người |
| `info` | trạng thái/bằng chứng được ghi nhận |

Sau đó soát PDF thực tế. Một báo cáo máy không lỗi không phải một lần đọc soát thị giác.

## Các vùng đọc soát bởi con người điển hình

Kiểm tra ít nhất các vùng liên quan tới ấn phẩm: độ chính xác văn bản, tham chiếu sự thật, tên và cơ quan người đóng góp, hệ phân cấp, dòng mồ côi/dòng goại, vị trí ghi chú, tính dễ đọc của khảo chú, sự đối ứng văn bản song song, chất lượng hình minh họa, chú đề, đầu trang, số trang, hành vi trang trắng, tính đúng của mục lục/chỉ mục, trang xuất bản và số trang cuối.

Với mã khung dùng chung đã thay đổi hoặc một đường cơ sở thị giác cố ý bảo toàn, người bảo trì cũng có thể dùng `pse visual-check`; so sánh thị giác là một tín hiệu soát xét, không phải một phán quyết thiết kế tự động.

## Ghi nhận các phát hiện cần soát

`pse release` chặn các chốt phát hành chưa xử lý. Khi chỉ còn các phát hiện `review` đã được soát và chấp nhận một cách có ý thức, người quản lý phát hành có thể dùng:

```text
pse release . --acknowledge-review
```

Cờ đó nghĩa là một người đã soát những phát hiện ấy. Nó không được dùng để vượt qua các phát hiện `error` hay biến một cuốn sách chưa soát thành cuốn đã duyệt.

Tiếp: [Bản đọc soát cho người nhận](recipient-proofs.md) hoặc [Chuẩn bị phát hành ấn bản](publication-release.md).
