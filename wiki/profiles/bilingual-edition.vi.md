# Ấn bản song ngữ

**Mã hồ sơ:** `bilingual-edition`  
**Phù hợp nhất:** ấn bản nguồn/bản dịch, ấn phẩm song ngữ đối chiếu, ấn bản dạy học ngôn ngữ, và các dự án khác nơi đoạn nguồn và đích phải giữ đối chiếu tường minh.

Hãy dùng hồ sơ khác với các sách dịch thông thường không cần đối chiếu nguồn/đích trong ấn phẩm phát hành.

## Hồ sơ cho cảm giác gì

Trình bày văn bản song song kiểu học thuật. Đối chiếu ngữ nghĩa ổn định kể cả khi bố cục hiển thị đổi giữa các chế độ cột, trang đối diện, khối tuần tự, hoặc nguồn/đích ưu thế.

Bộ trình diễn tích hợp của nó là `parallel-edition`. Chế độ hệ thống trang là `asymmetric-scholarly`, chế độ vật liệu bên là `outer-margin`, chế độ khảo chú là `available`, chế độ định vị là `source-defined`, và chế độ văn bản song song là `profile-controlled`.

## Mô-đun ngữ nghĩa

Mô-đun được bật bởi bản khởi đầu: `parallel-text`, `index`, `structural-hierarchy`, `contributor-metadata`.

Các mô-đun có chính sách tường minh cho hồ sơ này: `publication-unit-metadata`, `margin-objects`, `apparatus`.

| Mô-đun | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| `parallel-text` | bắt buộc | bật |
| `index` | khuyến nghị | bật |
| `structural-hierarchy` | khuyến nghị | bật |
| `publication-unit-metadata` | tùy chọn | tắt |
| `contributor-metadata` | bắt buộc | bật |
| `margin-objects` | khuyến nghị | tắt |
| `apparatus` | khuyến nghị | tắt |

`bắt buộc` nghĩa là hồ sơ phụ thuộc vào năng lực ngữ nghĩa ấy. `khuyến nghị`, `tùy chọn` và `không khuyến nghị` mô tả độ phù hợp biên tập; chúng không có nghĩa mọi tổ hợp về kỹ thuật khả thi đều đáng mong muốn.

## Bắt đầu từ các vùng dự án này

- `content/parallel.tex` — các đoạn nguồn/đích và quan hệ đối chiếu
- `config/bilingual-layout.json` — chọn chế độ trình bày mà không phải viết lại ngữ nghĩa đối chiếu
- `book.yml` và siêu dữ liệu người đóng góp — trách nhiệm ấn hành và dịch thuật

Tạo một dự án khởi đầu riêng tư bằng:

```text
pse new /path/to/private-projects --profile bilingual-edition
```

Sau đó chạy:

```text
pse build .
pse check . --human
```

Đừng chỉnh các tệp được sinh trong `build/` như nguồn bản thảo, và đừng sửa lõi dùng chung của PSE để tùy biến một cuốn sách duy nhất.

## Các điểm tùy biến hữu ích

- Chọn trong số `parallel-columns`, `facing-pages`, `sequential-blocks`, `source-dominant`, và `target-dominant`.
- Dùng ghi chú đối chiếu có kiểu và định vị đối chiếu ở nơi ấn bản cần.
- Khảo chú và vật thể lề có thể được kích hoạt mà không đổi ID đoạn.

## Ranh giới và giới hạn

- Vị trí trang hay cột không bao giờ là danh tính ngữ nghĩa của một đoạn.
- Đừng dùng hồ sơ chỉ để đặt hai cột văn bản không liên quan cạnh nhau.

## Bản demo tổng hợp

Kho chứa một dự án nguồn tổng hợp và PDF hoàn thành dưới:

```text
examples/profiles/bilingual-edition/
```

Từ thư mục gốc kho PSE, tạo lại bản demo đó bằng:

```text
python scripts/examples/build_profile_demos.py bilingual-edition
```

Bản demo dùng để hiểu hồ sơ, không phải một bản mẫu bản thảo để chép mù. Hãy bắt đầu một cuốn sách thật bằng `pse new` để siêu dữ liệu dự án, kích hoạt mô-đun và cấu hình được sinh vẫn mạch lạc.

## Các trang cẩm nang liên quan

Quay lại [tổng quan hồ sơ](index.md), hoặc tiếp tục với [Tạo lập và kiểm tra PDF](../getting-started/build-and-check.md). Với các tính năng như khảo chú, vật thể lề, văn bản song song hay định vị, xem [Tính năng sách](../book-features/index.md).
