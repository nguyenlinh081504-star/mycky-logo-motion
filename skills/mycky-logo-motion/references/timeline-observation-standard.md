# Tiêu chuẩn bóc tách video → TIMELINE TỔNG KẾT

## A. Xác minh thời gian

Một video có duration 4.67s, 133 decoded frames và nhịp trung bình ~30fps không chứng minh frame k nằm ở k/30s. PTS có thể giãn ở đầu, B-frame có thể thay đổi decode order, và VFR có thể giữ một frame trên nhiều tick. Dùng ffprobe -show_frames -show_entries frame=best_effort_timestamp_time,pkt_duration_time; với PTS bất thường, xem dữ liệu decoded presentation và thời lượng hiển thị. Mốc nên ghi: PTS, frame ordinal, frame trước/sau, sai số quan sát = khoảng frame lân cận.

Mọi thời gian:
- **OBSERVED:** frame và hành động nhìn thấy được, nêu khoảng, không khẳng định chính xác subframe.
- **INFERRED:** suy ra từ 2+ frame hoặc đo hình, ghi lý do và mức tin cậy.
- **PROPOSED:** bổ sung để khớp logo mới, ví dụ thêm wordmark sau clip thiếu tên.
- **UNKNOWN:** không thấy, bị che hoặc thiếu file. Không giả mốc.

Ví dụ một video mẫu kết thúc lúc icon chưa hiện chữ; các pha shrink→wordmark sau đó **phải được ghi PROPOSED**, không viết như đã quan sát.

## B. Cách tách đoạn 3 lớp

1. **Storyboard:** 10–25 trạng thái lớn; frame đầu/giữa/cuối. Ghi entry direction, hold, place, morph, draw, rotation, accent, shrink, wordmark.
2. **Microtimeline:** tập trung các pha khó ở mọi frame gốc hoặc 2–3 frame/mốc. Phân biệt hình thực tế đang thay đổi, opacity thay, và hình thật đã hoàn thiện. Đừng suy morph liên tục chỉ từ crossfade.
3. **Animation spec:** khoá source/target/ancestry, vị trí, progress function, ownership, index theo timeline 60fps, QA gate; luôn nói mốc nào là nội suy kĩ thuật.

## C. Template bắt buộc cho từng giai đoạn

### Phase N — start–end (OBSERVED / PROPOSED)
- **Frame/PTSs:** source frame hiện tượng đầu, frame kết thúc; nêu khoảng đo.
- **Tại đầu:** full pose của từng đối tượng; đối tượng nào đang đứng yên.
- **Chủ thể đang chuyển:** glyph, ảnh phụ, từng strand path hoặc parent group?
- **Từ đâu/đi đâu:** start/end position, trục dịch, hướng, pivot, anchor, head/tail; mô tả theo hình nhìn thấy.
- **Hình học:** một hay nhiều contour, counter, width, cubic, góc, junction, khe âm, nét bị che.
- **Sự kiện đồng thời:** đối tượng khác mờ đi hay lồng vào, nhưng không gom các sự kiện khác thành một "morph cả cục".
- **Kết thúc & nhịp:** trạng thái khớp frame cuối, velocity về 0 nếu có hold, cue để vào phase sau.
- **Cấm:** không tự font, không đổi hướng, không mọc path mới, không fade morph nếu brief không cho.
- **QA:** frame/mốc phải soi, loại lỗi quan trọng nhất, tolerance gắn với artwork thật.

## D. Các cửa sổ đặc biệt

**Entry glyph:** chữ đi ngoài khung vào và dừng; original silhouette hash/outline giữ nguyên; căn ink bbox. Không dùng ảnh nguồn kích thước 1000×2000 với khoảng trắng để tính center.

**Hold:** kiểm toàn bộ trạng thái glyph, không bồng bềnh, giãn, scale/rotation tween còn dư. Video mẫu có thời gian giữ dài không mặc định phải bỏ.

**Placement:** vị trí thay đổi để tương ứng với module đích, shape và scale khóa nếu brief yêu cầu; tách việc place với morph.

**Morph:** mỗi strand một source/target; C1/tangent, width và junction; không thay ảnh mảnh rời; nếu khối tham chiếu mờ đi là layer phụ thì ghi rõ opacity của **layer phụ**, không suy ra glyph morph bằng fade.

**Draw-on:** path source, startpoint, direction, arc-length, width profile, endpoint/cap; prefix tăng đơn điệu, chưa đi qua phải còn trống; nhiều nhánh có thứ tự.

**Rotation/clone:** pivot tính từ artwork, unwrap angle, giữ nguyên source khi quay nếu brief bắt buộc; nếu phần chỉ làm việc sau khi morph thì không vừa xoay vừa morph. Clone "con" có pose cha tại thời điểm sinh.

**Accent:** sao/crown/hoa tạo theo thứ tự chính; chỉ hiện sau gate mà video/brief xác nhận; sao di chuyển thì nét nối có endpoint bám theo nó, không tween endpoint độc lập.

**Group shrink:** một parent matrix cho toàn icon; scale đều; vị trí cuối khớp ảnh logo thật, không khớp frame tham chiếu của tên thương hiệu khác.

**Wordmark:** artwork nguyên dạng, kể cả dấu tiếng Việt; không dùng font tương tự hoặc tự tạo chữ, không hiện sớm khi icon chưa hoàn tất.

## E. Kiểm thử thời gian và nhịp

Dùng khung t_i là timestamp presentation. Nếu phase observed từ t_a tới t_b, dự báo frame ở 60fps là n đầu = ceil(t_a*60) và n cuối half-open = ceil(t_b*60), không làm tròn liên tục nhiều lần.

Đầu/cuối q: q=0 và q=1 phải khớp silhouette các pose đóng băng nếu phase giữ nguyên form. Qua những điểm 0,.1,.25,.5,.75,.9,1 thêm kiểm local + full. Mỗi phép đo có scale/coordinate system rõ ràng.

## F. Định dạng bảng tổng kết cho người dùng

| Bước | Giây mẫu | Độ chắc chắn | Nét/đối tượng | Hướng/chuyển động | Điều cấm |
|---|---|---|---|---|---|
| N | t0–t1 | OBSERVED | tên strand | nguồn→đích, nhịp, width | không tráo hình |

Sau bảng có **Timeline chi tiết có thể giao thẳng Codex**, không chỉ 1 câu/pha. Cuối bài ghi riêng những gì clip thực sự có và những gì thêm theo artwork (thường là logo name).

## G. Cảnh báo

Ảnh tham chiếu có búa, đống lửa, tạ hoặc con sóc chỉ là footage minh họa: không thể gọi bản thân ảnh phụ là glyph nguồn morph vào icon nếu nó thực tế chỉ mờ và biến mất. Những trường hợp user đã cung cấp glyph chính xác: phải ưu tiên file glyph gốc hơn hình glyph nhìn giống trong clip.
