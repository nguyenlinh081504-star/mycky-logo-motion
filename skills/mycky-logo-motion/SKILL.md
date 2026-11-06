---
name: mycky-logo-motion
description: "Use when a user supplies a logo or reference video for letter-to-icon animation, asks for multiple logical morph/rotation formulas in the style of @mycky1508, or needs fixes for tangled strokes, lost counters, contour jumps, clone assembly, pacing, sharpness, or final MP4 delivery."
---

# Mycky Logo Motion — từ chữ gốc thành icon có logic

Đây là skill cho **Codex có quyền đọc file, xem ảnh/video và sửa source**. Codex
hiểu hình bằng thị giác; script đi kèm đo hình, tách frame và kiểm tra file, không
giả là mô hình AI tự hiểu logo. Không có một phép morph chung đảm bảo mọi chữ
thành mọi icon đều đẹp. Mỗi nét phải có nguồn, đích và quá trình rõ ràng.

**Bản v2 có bài nhìn + video + code:** trước khi dựng hoặc sửa morph, đọc
[visual playbook](references/visual-playbook.md), mở bài đúng họ hình học trong
[SVG laboratory](references/visual-lessons.html), xem video và ảnh được liên kết.
Không chỉ đọc bảng công thức rồi tự nội suy cả contour. Đổi tốc độ một bản đã
đạt thì không cần học lại các bài hình học.

## Cổng hình học cho mọi logo mới

1. **Chuẩn bị chữ:** artwork → glyph rời đầy đủ → bản đồ màu từng vai nét →
   fit tĩnh icon. Chữ bị che cần phục dựng có căn cứ, không crop pixel rồi morph.
2. **Chọn theo anatomy:** trụ thẳng, bowl/counter, junction, ribbon, module lặp,
   nét vẽ. Từng formula trong catalog có `lesson_family` để tìm bài tương ứng.
   Không chọn chỉ theo tên chữ hoặc ép hình thành công thức quen tay.
3. **Khóa phần phải giữ:** source→target của từng vai, tim/đầu/đáy, tangent,
   width profile, crossing owner. Trụ thẳng ở cả hai đầu không tự biến thành
   gợn cao su ở giữa; chỉ cho cong khi target thật có lý do hình học đó.
4. **Thử đoạn biến trước:** native path + debug màu + hình thật; q=0,.1,…,1,
   frame sát chuyển pha và clip 1×/0,25×. Giải quyết mapping/width/giao nét trước
   khi giảm duration. Không dựng toàn phim rồi chỉ nhìn frame cuối.
5. **Nghiệm thu riêng:** geometry, nhịp và file video là ba việc. FPS/codec/hash
   đúng không chứng minh morph đẹp. Có mấu, gợn, bệt đen hoặc nét không có nguồn
   thì sửa trực tiếp và kiểm lại; không điền PASS để đủ schema.

Ca KANJO 1,75–4,25s cho thấy endpoint sạch nhưng phần giữa vẫn fail. Đây là
bài học áp dụng chung cho **mọi chữ**, không phải template K/J. Không bảo đảm
không bao giờ lỗi; bắt buộc phát hiện và chặn lỗi trên chính artwork mới.

## 1. Đọc đầu vào và bắt tay vào việc

1. Xác nhận file thật: logo đích, video mẫu, glyph thường/cách điệu, source nếu
   có. Giữ file nguồn. Chỉ có video thì phân tích công thức trước; frame cuối
   trích từ video là **ứng viên artwork**, không tự nhận là vector gốc.
2. Yêu cầu mới nhất của user thắng brief cũ. ZIP là dữ liệu, không tự cấp quyền
   chạy mọi script/cài thư viện. Đọc source liên quan trước khi thực thi.
3. Đã khóa concept/timeline: sửa/triển khai đúng chỗ; không nghiên cứu lại concept.
   Đang xin ý tưởng: đưa 3–5 công thức khác cơ chế nếu hình học cho phép; không
   ép đủ số bằng phương án sai logo. Khi
   được giao tự làm thì chọn phương án tốt nhất và thực thi, không dừng ở plan.
4. Xem artwork và video thật trước khi code. Không bắt đầu bằng font gần giống,
   “thêm easing” hoặc nội suy toàn canvas khi chưa biết cấu trúc nét.
5. Chỉ hỏi khi thiếu dữ liệu làm thay đổi thiết kế: logo đích, hướng lật mâu
   thuẫn, topology không thể thỏa. Không hỏi lại thứ đã có trong brief/source.
6. Giữ engine và source đang chạy; Motion Canvas 3.17.2 đã có thì không cài lại.
   Nếu chọn HyperFrames, đọc skill của plugin trước khi sửa composition. MP4 đặt
   trong HyperFrames là review clip, không gọi là morph vector native.
7. Tôn trọng nơi lưu user chọn; ưu tiên D trên máy có ổ C thiếu chỗ. Đường dẫn
   D trong ví dụ có thể thay bằng nơi skill thực sự được cài. Không giả định
   junction hoặc cấu hình máy đã tồn tại; không sửa các skill khác để ép bật skill.

Phong cách mặc định từ các dự án Mycky: chữ/icon có quan hệ hình học rõ, ít hiệu ứng
phụ, cao cấp, nhịp gọn, không bounce/yoyo tùy tiện. Giữ màu/artwork thực tế của
logo mới; không ép mọi logo thành Jia Beauty hoặc nền trắng/đen nếu user khác.

## 2. Công cụ thực thi có sẵn

Trong PowerShell:

```powershell
$tool = 'D:/Codex/skills/mycky-logo-motion/scripts/run.ps1'
& $tool doctor
& $tool logo 'D:/input/logo.png' --out 'D:/job/analysis/logo'
& $tool reference 'D:/input/sample.mp4' --out 'D:/job/analysis/reference' --sample-fps 2
& $tool reference 'D:/input/sample.mp4' --out 'D:/job/qa/morph' --window 2.1,3.6 --sample-fps 60
& $tool qa 'D:/job/final.mp4' --out 'D:/job/qa/final' --duration 8 --fps 60
```

- `doctor`: kiểm tra Python/OpenCV/FFmpeg đã có; không tự tải/cài. Vị trí runtime
  ở `runtime.local.json` (không commit); có mẫu `runtime.example.json`. Ưu tiên
  runtime/thư viện đang có, không tự tải hoặc cài lại.
- `logo`: đo **ink bbox**, tâm nét, thành phần và khoang âm; xuất mask/ảnh bbox.
  PNG alpha không bị coi nền trong suốt màu đen là khối đen. Auto không đúng thì
  dùng `--foreground dark|light|alpha`. SVG trả metadata; cần render bằng browser/
  engine có sẵn để nhìn/đo contour, không giả metadata là phân tích thị giác.
- `reference`: frame có timecode + contact sheet + các đỉnh thay đổi để soi.
  `--crop x,y,w,h` đo chỉ ROI logo tránh caption/watermark. Đỉnh metric có thể là
  morph, camera hay cut; Codex phải xem trước khi kết luận.
- `pair`: input JSON gồm `source`, `target` (vòng Nx2), `source_anchors`,
  `target_anchors` (index semantic theo thứ tự contour); xuất correspondence:
  `& $tool pair 'D:/job/pair.json' --out 'D:/job/paired.json'`.
  Thêm `--cubic-tolerance 0.5` để fit source/target thành cùng chuỗi cubic native,
  giữ mốc góc chung. Tolerance theo đơn vị input, chỉ là sai số mẫu fit, không
  phải chứng nhận Hausdorff hay thẩm mỹ. Raster staircase có thể sinh nhiều cubic;
  dựng lại các cung lớn/handle theo artwork trước khi gọi đó là vector tinh chỉnh.
  Render lại cả tiến trình và kiểm counter.
- `select`: kiểm điều kiện cứng rồi xếp hạng các đánh giá **có chứng cứ do Codex
  cung cấp**: `& $tool select 'D:/job/candidates.json' --out 'D:/job/decision.json'`.
  Không tự hiểu logo từ JSON/pixel hoặc chấm đẹp tự động. Xem mục 6.1.
- `qa`: giải mã toàn video, kiểm codec/kích thước/FPS/số frame/thời lượng, tạo
  decoded contact. `technical_pass` không phải nghiệm thu thẩm mỹ.
- `retime`: tăng tốc và giữ cuối, xem mục 10 để không cộng hold hai lần.

Có thể chạy `python scripts/logo_lab.py ...` trực tiếp. Cần NumPy/OpenCV/Pillow
đã có. Dùng `MYCKY_PYTHON_DEPS`, `MYCKY_FFMPEG`, `MYCKY_FFPROBE` để chỉ runtime
khác; launcher dùng runtime local nếu có, hoặc Python trên PATH. Không cài lại framework.

## 3. Xem video và biến quan sát thành công thức

1. Probe duration/FPS/kích thước; xem toàn clip. Một video kênh có thể có 4–6
   logo, phải tách từng logo thành segment, không học cả compilation như 1 morph.
2. Coarse contact 1–2fps → xác định đầu/cuối mỗi segment → xem 6–12fps ở segment
   → chỉ vùng khó mới lấy từng frame theo FPS gốc và playback 1×, 0,5×/0,25×.
   Video 30fps không có dữ liệu quan sát 60fps; đừng gọi nội suy là frame gốc.
3. Ghi các pha nhìn thấy: hướng vào, hold đọc chữ, placement, giản lược, morph,
   clone, góc/trục xoay, nét vẽ, accent, shrink, wordmark, hold cuối.
4. Phân biệt xoay phẳng với flip Y/ảnh soi gương. Đầu–cuối giống nhau không chứng
   minh số lần xoay; tăng mật độ mẫu ở khoảng xoay trước khi kết luận.
5. Mỗi segment lưu URL/file + timecode + glyph/brand nếu đọc được + công thức +
   invariant + điều chưa chắc + evidence. Caption/thumbnail không chứng minh motion.
6. Nhãn **observed** chỉ dùng cho điều nhìn thấy; cách dựng Bézier là suy luận
   kỹ thuật. Không nhận đó là source của người làm video mẫu.

Kênh: https://www.tiktok.com/@mycky1508. `references/channel-study.md` ghi video
đã xem và timecode; `references/channel-inventory.json` chỉ là link/caption đã
thu thập, **không phải tất cả đã xem**. Ảnh tại `assets/channel/` giúp đối chiếu.
Khi học tiếp, chọn các cơ chế còn thiếu, không chỉ đếm thêm video lặp.

Direct link lỗi nhưng profile mở được thì click video từ lưới để dùng player.
Đóng popup bằng nút thật khi cần. Bị đăng nhập/CAPTCHA/giới hạn thì ghi thiếu và
dùng file local user gửi. Không vượt kiểm soát truy cập, không tải remote media
để lách giới hạn hiển thị. Chụp frame player làm evidence được. Blur/cut/rung cạnh
của mẫu không phải chất lượng phải sao chép.

## 4. DNA hình học cần đo

Tách glyph thường, glyph cách điệu, icon, accent, wordmark/slogan. Không hard-code
hàng cắt icon/tên: hãy đo khoảng trắng thật để tránh cắt chân chữ dài.

| Mục | Cần ghi | Lỗi phòng tránh |
|---|---|---|
| Identity | đúng asset/font user cho phép | tự thay bằng font gần giống |
| Topology | outer/counter/components | B mất 2 khoang, O mất lỗ |
| Anatomy | thân/bowl/eo/bridge/leg/hook/serif/đuôi | morph cả cục không có logic |
| Landmark | đầu/cuối, góc thân, cực trị, junction | góc trong trượt sang đỉnh cung |
| Width | profile dày–mỏng, taper | cung trên phình, mảng đen |
| Registration | bbox nét/tâm/pivot/scale đều/đích | entry thấp, xoay lệch tâm |
| Symmetry | module có thật sự lặp/soi/180° | ép clone không khớp artwork |
| Ownership | nét nào sở hữu vùng giao | nét mọc/rút sai, đậm kép |

Tâm hiển thị tính theo **bbox nét thực**, không canvas PNG có mép trắng hoặc
baseline lockup cuối: `P_world=s*(P_local-pivot)+center`. Khi nhích entry/morph lên
theo user, cập nhật cả các pha liên quan; không chỉ dịch một frame đầu.

## 5. Thư viện nhiều công thức

ID là cơ chế có thể kết hợp, không phải preset ép mọi logo. Đọc điều kiện/hành
động/rủi ro ở `references/formulas.json`, nguồn/timecode ở channel study.

| ID | Chữ thường → icon | Điều kiện và invariant |
|---|---|---|
| F01 | Thu thân + mở serif | giữ tim/thân; không squash toàn chữ |
| F02 | B/P/D/R đổi bụng | outer và từng counter có mapping riêng |
| F03 | J/U mở móc, kéo mũi | chính mép móc trở thành đầu swash |
| F04 | V uốn thành module cánh | 2 chân có đích rõ và junction liền |
| F05 | X uốn thành 2 ribbon | vùng giao có trên–dưới nhất quán |
| F06 | S thành module xoáy/góc khung | eo không biến mất hoặc đứt |
| F07 | C mở thành cung ôm | bảo vệ đầu cung và khe hở |
| F08 | O đổi outer + inner | lỗ không sập thành khối đen |
| F09 | N rút đường chéo | giữ trụ; không tam giác thừa ở chân |
| F10 | A làm mảnh thanh ngang | co quanh tim thanh, không wipe chữ nhật |
| F11 | H trái xuống móc, phải lên cung | bridge nối cả 2 thân suốt morph |
| F12 | R đổi bowl và chân xiên | thân chỉ fade khi user cho phép rõ |
| F13 | K kéo chân thành đuôi | đuôi từ junction, không mọc rời |
| F14 | Y giãn nhánh + đuôi | junction 3 nhánh giữ liên kết |
| F15 | e mở loop, ghép vòng đôi | hiểu counter/khe mở trước khi ghép |
| F16 | Hai chữ dùng chung trục | CJ/ET/DR/FP… phân vùng thân trùng |
| F17 | Hai chữ đan vòng | DC/SK/SN… ancestry và giao rõ |
| F18 | Rút nét trùng trước ghép | MK/KM/KA/EB… chỉ bỏ nét có lý do |
| F19 | Đặt chéo vào registration rồi morph | JB/NA, scale khóa nếu brief yêu cầu |
| F20 | Một chữ phát triển 2 nhánh icon | tách theo cấu trúc thật, không xé vụn |
| F21 | Clone lệch song song | JJ, clone đúng asset trước khi tách |
| F22 | Clone xoay Z 180° | chỉ clone xoay khi brief khóa |
| F23 | Clone lật Y 0→180° | một chiều, đúng một lần, không yoyo |
| F24 | Lặp 3 module 120° | chứng minh fit đối xứng bậc 3 |
| F25 | Lặp 4 module 90° | S/H/V hoa/khung, tâm không đen cục |
| F26 | Hai module xoay lệch khóa nhau | T/e/O dạng đôi, pivot đúng |
| F27 | Đầu nét phát triển vòng bao | Y/TJ/ET, liên tục theo arc |
| F28 | Một bút vẽ chuỗi loop | The Phia, chưa tới bút thì còn trắng |
| F29 | Vẽ trụ/serif từ nút gắn | VN/PL, không đốm rời ở junction |
| F30 | Khoang âm thành silhouette | Q + chân dung, chỉ nếu artwork có |
| F31 | B thành ribbon/đuôi dài | BLING, counter chuyển có logic |
| F32 | Rút cầu nối sau morph | JB, chỉ cầu tạm; bảo vệ đáy B |
| F33 | Ảnh ý niệm → tim nét → icon | yoga/bông/cafe; chỉ khi user muốn |
| F34 | Accent sau khi icon khớp | sao/kim cương/crown; thời điểm theo brief |
| F35 | Icon+accent thu về lockup | một parent matrix, giữ tương quan |
| F36 | Wordmark hiện nguyên cụm | nếu user yêu cầu, không wipe dọc/stagger |
| F37 | Chữ thành dải sóng song hành | N/n/W, module gốc rồi clone/offset có căn cứ |
| F38 | Chữ + đuôi thành infinity | SQ, phải soi dày để gán ownership hai loop |
| F39 | Khung chữ nhật mọc từ trụ | YC, khung có trong artwork và gắn đúng nút |
| F40 | Radial k module tùy logo | đếm cánh thật, không ép mọi logo bậc 4 |
| F41 | Ghép theo lưới vuông góc | LTT, giữ trục/khoảng cách/width chuẩn |
| F42 | Ba chữ dùng chung diagonal | NYX/ARN, mapping từng nét trước khi ghép |

Không chọn bằng tên chữ đơn thuần: B có thể F02 hoặc F31; G có thể vòng mở hoặc
module lật. F30/F33 không được tự thêm vào concept chữ đã khóa. Module cứng chỉ
fit gần đúng thì báo sai khác và điều chỉnh contour tối thiểu trong pha cho phép;
không tráo target ở cuối. Công thức chỉ thấy một lần không thành luật mọi logo.

## 6. Đề xuất 3–5 phương án có thể dựng

Chọn 3–5 mẫu nguồn cùng cấu trúc. Mỗi phương án khác cơ chế, không chỉ khác
hướng entry. Ghi bảng:

```
Tên + ID; nguồn URL/file + timecode đã xem.
Thân/eo/bowl/đuôi/counter/junction nào → phần nào của icon.
Thứ tự pha: vào → hold → đặt → morph → lắp/vẽ → accent → thu → tên.
Topology nào giữ, thay đổi nào có chủ ý; không biết thì ghi chưa chắc.
Pivot/trục/góc/số clone; phần nào cố định.
Nhịp và thời gian giữ; vùng dễ lỗi và cách kiểm.
Quan sát được / suy luận kỹ thuật / thiếu asset.
```

Ưu tiên ancestry rõ, ít đổi topology, ít ownership tranh chấp, khớp artwork và
đọc được chuyển động. Loại phương án cần xé chữ vô nghĩa, kéo góc thân vào cung,
hoặc fade/blur giấu thiếu nét. Xin ý tưởng thì chỉ làm ý tưởng; xin thực hiện thì
triển khai, không bắt user duyệt lại những bước đã giao tự làm.

### 6.1 Từ một logo mới: chọn công thức nào phù hợp nhất?

Không chọn theo tên chữ B/J/G hay số lượt dùng preset. Chọn theo thứ tự:

1. **Khóa đích:** đăng ký artwork đúng tỷ lệ, tách glyph/icon/tên; ghi counter,
   nhánh, điểm nối, nét mảnh và module lặp thật. Chỉ có logo đích thì suy luận
   nguồn từ chính cấu trúc đó; không tự khẳng định font thường chính xác nếu
   không được cung cấp. Tên thương hiệu chỉ gợi ý chữ nguồn, không quyết định cơ chế.
2. **Thử lắp hình tĩnh:** một module qua scale đều/rotation/translation/flip có
   khớp phần còn lại không? Dùng sai số contour đã register và nhìn overlay.
   Module khác hình không được gọi là clone; không có lặp thì loại radial.
   Có hai counter thì ưu tiên cơ chế bảo toàn cả hai; có bridge thì cần mapping
   giữ nối; có nét vòng sẵn thì có thể draw-on, không buộc mọi icon quay.
3. **Lập shortlist:** thường 3–5 công thức hoặc cách phối cơ chế, mỗi phương án
   có bảng nguồn→đích từng nét. Chỉ một phương án hợp hình thì dùng một; không
   tạo nhiều concept yếu để đủ số. Brief đã khóa thì không tổ chức cuộc thi
   concept: chỉ tối ưu mapping/nhịp trong đúng công thức được giao.
4. **Loại trước khi chấm:** sai artwork, mất counter không chủ ý, nét không có
   nguồn, bridge đứt, thứ tự sai hoặc sinh nét thừa đều loại. Điểm nhịp đẹp không
   bù được lỗi này. Điều chưa kiểm phải là `null`/pending, tuyệt đối không điền
   sẵn `true` từ script. Topology change chủ ý cần ghi rõ invariant theo từng pha.
5. **Đánh giá có căn cứ:** khớp đích 30%, liên tục anatomy 25%, sạch hình 20%,
   nhịp 15%, hợp phong cách mẫu 10%. Đây là trọng số thực hành, không định luật.
   Mỗi điểm 0–1 phải kèm timecode/frame/overlay và lý do, không bịa số để thắng.
6. **Kiểm chuyển động trước khi chọn:** render đoạn khó của ứng viên có căn cứ
   nhất; nếu còn hai phương án ngang nhau hoặc mapping chưa chắc thì chỉ test
   2–3 đoạn ngắn cần phân biệt, không render nhiều phim đầy đủ. Xem 1× và 0,25×,
   từng frame ở chuyển pha. `visual_review=pass` chỉ sau khi thực sự xem.
   Lệch điểm <0,03 là gần ngang: xem lại đoạn quyết định hoặc cân nhắc nhịp user,
   không tự tuyên bố có một đáp án tối ưu tuyệt đối.
7. **Chọn và nói ngắn:** “Chọn Fxx vì [đặc điểm hình học + nét nào giữ được];
   loại Fyy vì [lỗi cụ thể].” Chỉ gọi là **phù hợp nhất trong các phương án đã
   kiểm tra**. Không hứa logo bất kỳ đều được tự động phân tích chính xác 100%.

`references/selection-template.json` là input trống có PENDING cho helper.
`rank_candidates()` chỉ kiểm gate/tính trọng số, không nhìn thay Codex. Chuỗi
“pass” không phải bằng chứng nếu chưa có frame/playback thật. Rủi ro còn thiếu
asset hoặc vùng hình học chưa kiểm phải giữ pending; tiếp tục xử lý, không ship.
Helper yêu cầu file artwork thật, invariant riêng của logo và lý do fit anatomy;
các công thức có `requires_repeated_module` trong catalog cần overlay chứng minh
lặp. Placeholder PENDING/TODO không được tính là bằng chứng. Kiểm helper bằng
`python scripts/self_test.py`; file tạm theo `scratch_root` trong runtime local.

Ví dụ: B có hai khoang, đích vẫn là một B bất đối xứng → F02 + F31 nếu có đuôi,
không tự chọn F25 bốn cánh. Một module B giống nhau lặp đúng bốn góc → F02 hoàn
thành trước, rồi hold/căn pivot → F25. Cùng chữ B nhưng hai logo dùng hai công
thức khác nhau vì **cấu trúc đích** khác nhau.

### 6.2 Hiệu chuẩn kiểm tra theo chính artwork

Đo ở độ phân giải giao cuối và thêm lượt 2–4× để soi mép. Đo source/target qua
cùng rasterizer trước: dùng sai lệch raster này làm mức nền cho tolerance, không
ép một ngưỡng px vào mọi logo. Lưu min width và diện tích từng counter theo
q; biến thiên phải khớp ý đồ, không đột ngột về 0 rồi mọc lại. Mỗi junction có
ROI và invariant riêng; silhouette IoU tốt không bỏ qua bridge bị đứt.

Ví dụ học được trong `assets/examples/B-*`: hai counter được gán mốc thân/eo/
đỉnh/đáy riêng, không ghép bằng điểm cao nhất tùy tiện. Chạy:
`python scripts/b_counter_example.py --out D:/job/qa/B-example`.
Ví dụ kiểm 101 trạng thái, xuất input `pair` cùng anchor report/contact; dùng
`pair --cubic-tolerance` để dựng cubic. Đây là minh họa với **hai asset cụ thể**,
không tái sử dụng tọa độ/mốc index cho B của khách khác hoặc coi test số thay
nghiệm thu chuyển động native cuối.

## 7. Thuật toán morph chuẩn

### 7.1 Semantic correspondence và endpoint

1. Đưa mỗi glyph về local coordinates. Trace source/target; tách outer và từng
   counter. Winding/fill-rule nhất quán; không đảo mỗi counter một cách tình cờ.
2. Ghép landmark **cùng nghĩa**: góc trong thân trên↔góc trong thân trên, eo↔eo,
   đầu móc↔đầu móc. Không lấy min(x,y) trên mỗi contour làm cùng mốc: đỉnh cao
   nhất counter dưới B nằm trên cung sẽ gây wedge như lỗi JIA.
3. Chia contour theo các cặp landmark, resample arc-length **từng section**.
   Hợp mọi arc knot của cả hai đầu để giữ đủ vertex/góc. Helper `correspond()`
   làm phần này, không tự suy luận anatomy.
4. `P_i(q)=(1-q)*S_i+q*T_i`. Với cubic đã fit: nội suy endpoint/control points
   có cùng mapping. C1/G1 tại nút mềm; không ép smooth góc serif chủ ý sắc.
5. Render p=0 và p=0+ cùng hệ raster/coverage. Đừng dùng mask nguyên ở 0 rồi
   polygon downsample ở 0+ khiến nháy rìa. Contour phải khớp đích **trước cleanup**.
6. B: outer/upper counter/lower counter riêng; compound path một lần với even-odd
   hoặc winding đúng. Không đổ đen rồi xóa lỗ làm mất rìa. Kiểm số khoang/diện
   tích/cổ hẹp suốt tiến trình, không chỉ đầu–giữa–cuối.

SDF toàn canvas không phải cách né mapping. Level-set có thể dùng khi topology
thực sự đổi nhưng dễ sinh đảo/đuôi rời; phải có miền kiểm soát và QA. Topology
change không thể đồng thời là bijection C1 mọi nơi; không hứa điều bất khả.

### 7.2 Dày–mỏng, junction, ownership

Với tim `C(s)`, pháp tuyến đơn vị `N(s)` và width `w(s)`:
`L=C-w*N/2`, `R=C+w*N/2`. Nội suy tim, tangent và width có liên kết. Width dương
ở thân, chỉ về 0 tại taper có chủ ý. Offset ở cong gắt có thể tự giao: sửa
handle/tim/width, không đắp thêm nét. So cung trên/dưới ở cùng scale.

- H: bridge endpoint lấy từ hai thân đang morph; không tween riêng làm tuột nút.
- Giao: union/ownership chủ ý, không cộng alpha. Mảng đen lạ là geometry/overlap
  chứ không giải quyết bằng thêm easing.
- Cleanup: mask/path chỉ thuộc cầu tạm, sau morph, không whole-icon morph. Bảo
  vệ official stroke và đáy chữ; pixel đã rút không mọc lại ở pha sau.
- Fade chỉ cho exit/accent/text hoặc nét user cho phép rõ (thân R CARINR). Không
  suy rộng ngoại lệ này sang morph khác.

### 7.3 Draw-on theo bút

Tạo LUT arc-length qua mọi cubic; tại p tìm đoạn/tham số đạt `p*L_total`, cắt
cubic bằng de Casteljau. Với fill thư pháp: miền bút chạy theo tim giao silhouette
gốc. Mask quá rộng ở giao nét sẽ lộ đoạn chưa tới, phải sửa miền reveal. Nét đã
vẽ giữ nguyên; chưa tới còn trắng. Circle theo đúng hướng/startpoint, không bật
bốn góc hoặc full ring cùng lúc. Serif bắt đầu từ nút gắn, không đốm rời.

## 8. Clone, pivot và xoay

Morph xong → hold → căn góc/scale/vị trí nếu có → hold → clone trùng khít → tách/
xoay. Không vừa morph vừa rotate khi brief khóa hai pha. Clone tạo một lần, không
nhân lại mỗi renderAt. Nếu yêu cầu clone xong mới rút nét thì giữ nguyên nét lúc
clone bắt đầu. Bản gốc không xoay khi user chỉ cho clone xoay.

Xoay phẳng: `P'=c+R(theta)*(P-c)+translation`.
Radial: `theta_j=theta0+2*pi*j/k`, fit union k module vào artwork trước khi chọn.
Flip Y trực giao: `x'=cx+cos(theta)*(x-cx)`, `y'=y`, theta 0→pi một chiều. 90°
bề ngang gần 0 đúng chiếu cạnh; không tráo hình khi đang nhìn chính diện.
Flip Y **khác** rotation Z 180°. Mỗi property có một timeline owner tại một thời
điểm; không tween chồng làm đổi chiều/bounce ngoài ý muốn.

## 9. Nhịp nhanh nhưng mềm và pipeline nghiệm thu

Sửa geometry trước, timing sau. Một q(t) chung cho các nét đang liên kết.
Smootherstep `6u^5-15u^4+10u^3` hợp move/settle. Morph có cảm giác chờ thì dùng
velocity ramp 15–20% đầu/cuối, giữa gần đều (`motion_progress()`); không đẩy hết
chuyển động vào giữa bằng easing bậc cao. Nếu biến dạng vẫn chênh tốc độ: đo
visible union changes, làm mượt **chuỗi metric**, tích phân L(q), nghịch đảo đơn
điệu q=L^-1(s(t)). Đây là time warp, không blur hình. Không plateau/reverse.

Adapter engine cần `renderAt(t)` deterministic:

```text
u=clamp((t-phaseStart)/phaseDuration,0,1); q=motionProgress(u)
for glyph + its counters: interpolate matched paths, draw compound fill
apply node/group matrix once; reveal only paths whose phase has started
```

Motion Canvas: native Path/Bézier data từ progress, refs original/clone riêng;
kiểm API trong package đã cài. HyperFrames: một GSAP timeline seekable, đăng ký
`window.__timelines`, SVG path dưới parent; không setInterval. Không cài plugin
MorphSVG/DrawSVG chỉ vì skill có nhắc nếu không có/không cần.

**Vòng nghiệm thu:**

1. Fit source/target tĩnh và module transform trước. Không fit thì chưa render phim.
2. Render riêng pha khó. So từng frame quanh morph-start/end, junction đổi chủ,
   clone-start, góc 90°, cleanup, shrink-end. Contact **và** playback 1×/0,25×.
3. Ghi timecode/vùng/giả thuyết lỗi. Sửa đúng correspondence, control point, width,
   ownership hay time warp; render lại cửa sổ lỗi trước, không full render liên tục.
4. Fail nếu counter sập sai, bridge đứt, đảo rời, gai/đầu mọc sớm, mảng đen lạ,
   contour trượt, trục/số xoay sai, mất đáy B, icon chưa khớp mà đã hiện tên.
5. Pha khó đạt mới xuất toàn bộ; giải mã MP4, xem cả đầu/cuối/chuyển pha/wordmark.
   So final với artwork đã register. IoU/binary giống không chứng minh đẹp:
   soi viền, nét mảnh, khoảng âm, phóng 2–4×, đọc ở kích thước xem bình thường.
6. Chống răng cưa: sửa trace trước, coverage subpixel hoặc vector oversample rồi
   downsample tốt. Không Gaussian blur để giấu lỗi; phân biệt preview scale thấp.
7. Mặc định lịch sử: H.264 High level 4.2, yuv420p, faststart, 1080×1920, 60fps,
   8s = **480 frame**. User khác thì theo user. Tránh qp=0/High444 lỗi player.
8. User chỉ muốn 1 MP4 thì chỉ gửi 1 MP4; source/evidence/QA nội bộ. Không tuyên
   bố hoàn hảo. Còn lỗi thì nói rõ phạm vi, không gửi bản cho có.

## 10. Tăng tốc 2×/2,1× và giữ cuối

Tốc độ khác oversample độ phân giải. 8s ở 2× → 4s, 240 frame 60fps; không đổi
1080×1920. Tăng tốc bản đã đạt thì retime đủ tốt, không cần full render lại.

```powershell
& $tool retime 'D:/job/final.mp4' 'D:/job/final-2x.mp4' --speed 2
& $tool qa 'D:/job/final-2x.mp4' --out 'D:/job/qa/2x' --duration 4 --fps 60
```

Muốn logo xong đứng yên 1s: xem **frame đầu hoàn thiện toàn bộ logo** t_complete,
thay hold cũ: `T_out=t_complete/speed+hold` (làm tròn frame).

```powershell
# Logo xong tại 7s của video 8s: 7/2+1 = 4.5s = 270 frame.
& $tool retime 'D:/job/final.mp4' 'D:/job/final-2x-hold1.mp4' --speed 2 --complete-at 7 --hold 1
```

Không có complete-at thì hold là **nối thêm**, còn hold cũ cũng bị tăng tốc. Không
tự cộng nhầm hai lần. Helper không ghi đè nguồn. Video có audio: atempo hợp lệ
và kế hoạch đuôi nhạc rõ khi hold đổi; không tự cắt/kéo nhạc. Silent giữ silent.

## 11. Tài liệu sống

- `references/channel-study.md`: video TikTok thực sự đã xem, mốc và quan sát.
- `references/formulas.json`: điều kiện, từng bước, rủi ro, nguồn từng công thức.
- `references/visual-playbook.md`: 7 họ, video/ảnh, vai nét, constraint và cách code.
- `references/visual-lessons.html`: native SVG deterministic, scrub và debug màu.
- `references/geometry-contract.completed-example.json`: spec đã điền của bài học.
- `references/reference-video-ledger.json`: video tham chiếu thật + cửa sổ cần xem.
- `examples/counter-motion-canvas.tsx`: scene native 3.17.2, compound winding đúng.
- `references/selection-template.json`: gate, điểm có chứng cứ và quyết định chọn.
- `references/motion-contract.example.json`: mẫu ancestry/phase/pivot/QA để triển khai.
- `references/channel-inventory.json`: danh mục link, không đồng nghĩa đã xem.
- `references/case-lessons.md`: sửa lỗi VN/PHIA/OHANA/NA/GX/PL/CR/LUMI/BÍCH/BLING/JIA.
- `assets/channel/`: ảnh chứng cứ, không artwork dùng thay logo của dự án mới.

Học thêm bằng review mẫu thiếu cơ chế, ghi timecode/evidence và mở rộng catalog.
Không biến sở thích riêng một logo thành luật toàn bộ. Tự hỏi trước kết luận:
đã nhìn frame thật chưa; từng nét nguồn→đích rõ chưa; công thức hợp artwork hay
chỉ cùng tên chữ; thứ tự đúng chưa; MP4 thực tế đã xem chưa?
