# Production Director — quy trình từ video mẫu đến MP4

> Phụ lục vận hành cho skill mycky-logo-motion v2.1. Đọc khi nhận video mẫu, ảnh glyph nguồn, logo đích hoặc một project cần sửa. **Không thay SKILL.md và các cơ chế F01–F42.**

## 0. Hợp đồng công việc

Đầu vào: (a) video tham chiếu, (b) artwork đích; (c) ảnh chữ gốc nếu khách cung cấp; (d) source/ZIP cũ nếu có; (e) yêu cầu thời lượng, canvas, FPS. Ưu tiên phần khách đã khóa hơn video mẫu lỗi. Không tự dựng lại concept nếu đã có project đúng.

Đầu ra theo mục đích:
- **Phân tích:** timeline chuẩn hóa + anatomy/ownership + ảnh chứng cứ + phần chưa chắc; không tự nhận đã render.
- **Triển khai:** source deterministic + bản render cửa sổ khó + QA.
- **Bàn giao cuối:** MP4 mở được, đối chiếu logo đích; nếu user chỉ muốn MP4 thì chỉ gửi MP4, giữ nội bộ source, QA.

## 1. Quy trình 12 bước có điều kiện dừng

1. **Kiểm và phân loại tài sản.** Ghi tên thật, kích thước, nguồn, hash, có quyền sử dụng không; phân biệt hình gốc, icon đích, wordmark, video mẫu, footage minh họa. Một ảnh cuối không đủ để khẳng định font glyph đầu.
2. **Tạo scene inventory.** Xác nhận kích thước, codec, số frame giải mã, PTS thực, duration, VFR/giãn frame và tiếng. Nếu có frame kéo dài thì lấy timestamp per-frame, không suy thời gian bằng index / 30.
3. **Trích bằng chứng.** Contact sheet toàn clip 0.15–0.25s, thêm từng frame ở cửa sổ morph, đường vẽ, crossing, rotation, frame ngay trước/sau chuyển pha. Xem ảnh phóng lớn và playback 1×/0.25×. Không suy từ một ảnh cuối.
4. **Ghi kịch bản quan sát.** Mỗi phase có start/end, frame/PTS, đối tượng, trạng thái đầu/cuối, điểm đầu chuyển động, hướng, pivot, opacity, hold, sự kiện phụ thuộc. Phân riêng OBSERVED / INFERRED / PROPOSED / UNKNOWN.
5. **Tách artwork đích.** Đăng ký logo theo ink bbox, không theo khoảng trắng của canvas PNG. Tách icon, từng glyph, counters, nối, dấu, star/flower/crown và wordmark. Kiểm overlay ở kích thước xuất.
6. **Dựng ancestry / stroke ownership.** Bảng nguồn→đích cho từng semantic strand. Trụ, bowl, hook, counter, serifs, leg, ribbon, cầu tạm, hình trang trí phải có chủ sở hữu. Giao nét luôn ghi lớp trước/sau, junction và thời điểm được thay đổi topology.
7. **Chọn cơ chế từ F01–F42.** Chọn theo anatomy và thứ tự video, không vì tên chữ. Ví dụ: chữ C/M lồng → F16/F17/F19; thanh vẽ → F27/F28/F29; cầu rút sau morph → F32; group shrink → F35; wordmark → F36. Nếu logo không có module lặp, không ép clone/radial.
8. **Fit hai đầu và pose trung gian.** Fit source pose, target pose, khoảng trắng, các section cubic và trụ thẳng trước khi chạy easing. Dựng frame biên pha cùng renderer/fill rule, so coverage q=0 và q=0+.
9. **Dựng theo phase owner.** Entry giữ glyph gốc, hold tĩnh, place nếu có, morph có nghĩa, hold, vẽ/lắp/clone, accent, shrink, wordmark, hold cuối. Mỗi property (x/y/rotation/scale/shape) chỉ có một timeline owner trên một khoảng.
10. **Kiểm cục bộ trước.** Chọn cửa sổ khó nhất (morph, giao nét, nét vẽ, xoay), render ngắn, nhìn frame + clip 1×/0.25×, sửa từng vấn đề có timecode. Không render lại full liên tục để che lỗi.
11. **Kiểm video cuối.** Giải mã H264, đúng dimensions, fps, duration, nb_frames; soi frame giữa, frame đầu/cuối, phase boundaries, chữ dấu, so target overlay. Đạt kỹ thuật khác với đạt thẩm mỹ. Không điền PASSED khi chưa xem.
12. **Bàn giao gọn.** Bàn giao đúng số file user yêu cầu, có link tải thực và kiểm file tồn tại. Với handoff Codex: ZIP đủ brief/timeline/assets/source/QA và một lệnh ngắn tập trung lỗi; không đưa CODEX quay về nghiên cứu lại concept.

## 2. Chính sách khớp video và sửa lỗi video mẫu

**Video mẫu là chứng cứ về thứ tự/nhịp, không nhất thiết là chuẩn chất lượng.**
- Giữ chuyện gì xảy ra trước/sau, vị trí nguồn→đích, góc/pivot tương đối, đoạn hold đặc trưng.
- Không sao chép rung, popping, mất nét, bệt đen, méo, watermark, phụ đề, font khác hoặc frame nén lỗi.
- Nếu tài liệu gốc không cho biết PTS/trạng thái chính xác: ghi độ bất định; không tuyên bố tính được chuyển động 0.00001 giây từ video 30 FPS.
- Nếu footage là logo thương hiệu khác: theo đúng choreography có thể kiểm chứng, nhưng thay đích bằng artwork khách và nói rõ các phase bổ sung.

## 3. Cửa ưu tiên khi giảm token

Ưu tiên (i) đọc brief + file spec, (ii) nhìn 12–20 keyframe tiêu biểu, (iii) chỉ mở source của đoạn lỗi, (iv) render cửa sổ 0.5–1.5s, (v) QA, (vi) full render cuối. Không cài lại môi trường, không thử 5 concept khi brief đã khóa, không tạo slideshow thay animation.

Giao việc có độ chính xác cao: yêu cầu Codex chỉ sửa phần lỗi, giữ nguyên các pha đã đúng, nhưng tự tìm nguyên nhân và kiểm toàn video trước khi giao.

## 4. Nơi tra cứu

- [timeline-observation-standard.md](timeline-observation-standard.md): đo PTS và viết timeline 17–20 pha.
- [geometry-morph-contract.md](geometry-morph-contract.md): map section, chân/đầu, Bézier, counter, junction, điểm chia.
- [production-qa-token.md](production-qa-token.md): cổng QA và tiết kiệm token.
- [production-casebook.md](production-casebook.md): case cụ thể từ những dự án vừa phân tích.
- [codex-handoff-pack.md](codex-handoff-pack.md): prompt và cấu trúc ZIP.
- ../scripts/timeline_evidence.py: tiện ích trích PTS và contact sheet; không khẳng định tự nhận biết anatomy.
