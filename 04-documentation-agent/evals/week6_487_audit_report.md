# الأسبوع السادس — تدقيق 487 حالة من نتائج التقييم الاصطناعي

## نطاق التقرير وحدوده
تمت قراءة 487 سجلًا من ملف النتائج. هذا **فحص آلي مستقل للوقائع القابلة للاستخراج من الملف**، وليس حكمًا بشريًا موثقًا على جميع الإجابات. ملف النتائج يحوي السؤال والمرجع والإجابة وسجل أسماء الأدوات وأحكام الـ Judges، لكنه لا يحتوي محتويات جميع الوثائق المسترجعة ولا يثبت ما إذا كان النموذج شرح سبب استخدام الأدوات في وقت الاستدعاء.

## النتائج المثبتة
- الأحكام الإجمالية للـ Judges: صحة الإجابة 275 Good و212 Bad؛ اتباع التعليمات 399 Good و88 Bad؛ مسار الأدوات 401 Good و86 Bad.
- وردت كلمة `pip` في 31 إجابة رغم أن System Prompt يمنع ذكرها. هذا انتهاك نصي واضح.
- صنّف Instruction Following Judge عدد 15 من هذه الإجابات على أنها Good رغم ظهور `pip`. هذا تعارض يمكن التحقق منه مباشرة.
- توجد 4 حالات بها استدعاء أدوات مكرر حرفيًا. التكرار ليس بالضرورة خطأ، لكنه يستحق التحقيق.
- الملف الذي ولّد الإجابة المرجعية استُرجع ضمن أدوات الـ Agent في 230 حالة، ولم يُسترجع في 257 حالة. ليس من الصحيح عدّ الغياب خطأً تلقائيًا؛ قد يوجد الجواب في مصدر بديل.

## أمثلة يمكن التحقق منها
- الحالة 1: ذكر `pip install` بينما ادعى Instruction Judge عدم مخالفته تعليمات `uv` (Good). التقييم البشري المصرح به في المحادثة: Correctness=Good وInstruction=Bad وTrajectory=Good.
- الحالة 18: إجابة إعداد Evidently Cloud تحتوي `pip install`، وحكم Instruction Judge=Good.
- الحالة 180: استرجاع `faq/telemetry.mdx` مرتين مع بقاء Trajectory Judge=Good؛ ضرورة التكرار تحتاج فحصًا.
- الحالة 2: إجابة إنشاء Data Drift Report تحتوي جوهر الإجابة المرجعية، ومسار الأدوات يبدأ ببحث ثم استرجاعين؛ لم تُحسم صحة التفاصيل الإضافية مقابل الوثائق الأصلية.

## الحالات ذات الأولوية للمراجعة البشرية
اخترت أولًا حالات التعارض النصي التي فاتت على Judge، ثم التكرارات، ثم أمثلة مرجعية متنوعة. هذه قائمة مرشحة للمراجعة، وليست عينة عشوائية تمثل كل الـ487 حالة.

| الحالة | أحكام C / I / T | سبب الأولوية |
|---:|---|---|
| 1 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 18 | bad / good / bad | ذكر pip رغم حكم الالتزام Good |
| 68 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 86 | bad / good / good | ذكر pip رغم حكم الالتزام Good |
| 90 | bad / good / good | ذكر pip رغم حكم الالتزام Good |
| 151 | bad / good / good | ذكر pip رغم حكم الالتزام Good |
| 152 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 177 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 187 | bad / good / bad | ذكر pip رغم حكم الالتزام Good |
| 271 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 286 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 294 | bad / good / good | ذكر pip رغم حكم الالتزام Good |
| 408 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 449 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 459 | good / good / good | ذكر pip رغم حكم الالتزام Good |
| 42 | good / good / bad | استدعاء متكرر |
| 180 | good / good / good | استدعاء متكرر |
| 251 | bad / good / bad | استدعاء متكرر |
| 417 | good / good / bad | استدعاء متكرر |
| 2 | good / good / good | مراجعة مرجعية |

## سجل الحالات الـ487
في الجدول التالي: C=صحة الإجابة، I=اتباع التعليمات، T=مسار الأدوات. ظهور `pip` انتهاك ثابت، بينما أرقام Judges تبقى أحكامًا غير مؤكدة بشريًا.

| # | C | I | T | pip | تكرار أدوات | ملف المرجع مسترجع |
|---:|---|---|---|---|---|---|
| 1 | good | good | good | نعم | لا | نعم |
| 2 | good | good | good | لا | لا | لا |
| 3 | good | good | bad | لا | لا | نعم |
| 4 | bad | good | good | لا | لا | لا |
| 5 | good | good | good | لا | لا | نعم |
| 6 | bad | bad | good | لا | لا | لا |
| 7 | good | bad | good | لا | لا | لا |
| 8 | bad | good | good | لا | لا | لا |
| 9 | good | good | good | لا | لا | لا |
| 10 | bad | bad | good | لا | لا | لا |
| 11 | good | good | good | لا | لا | لا |
| 12 | bad | good | good | لا | لا | لا |
| 13 | good | good | good | لا | لا | لا |
| 14 | good | good | good | لا | لا | نعم |
| 15 | bad | bad | good | لا | لا | لا |
| 16 | good | good | good | لا | لا | نعم |
| 17 | good | good | good | لا | لا | نعم |
| 18 | bad | good | bad | نعم | لا | لا |
| 19 | good | good | good | لا | لا | نعم |
| 20 | bad | bad | good | لا | لا | نعم |
| 21 | good | good | good | لا | لا | نعم |
| 22 | bad | good | good | لا | لا | لا |
| 23 | good | bad | good | نعم | لا | لا |
| 24 | bad | good | good | لا | لا | لا |
| 25 | good | good | good | لا | لا | نعم |
| 26 | good | good | good | لا | لا | لا |
| 27 | bad | good | good | لا | لا | لا |
| 28 | bad | good | bad | لا | لا | نعم |
| 29 | bad | good | good | لا | لا | لا |
| 30 | bad | good | bad | لا | لا | نعم |
| 31 | bad | bad | good | لا | لا | لا |
| 32 | bad | good | bad | لا | لا | لا |
| 33 | good | bad | bad | لا | لا | نعم |
| 34 | good | good | good | لا | لا | لا |
| 35 | good | bad | good | لا | لا | لا |
| 36 | good | good | bad | لا | لا | نعم |
| 37 | good | good | good | لا | لا | نعم |
| 38 | good | good | good | لا | لا | نعم |
| 39 | good | good | good | لا | لا | نعم |
| 40 | bad | good | good | لا | لا | لا |
| 41 | bad | good | good | لا | لا | لا |
| 42 | good | good | bad | لا | نعم | نعم |
| 43 | bad | good | bad | لا | لا | لا |
| 44 | good | good | good | لا | لا | لا |
| 45 | bad | bad | good | لا | لا | لا |
| 46 | good | good | good | لا | لا | نعم |
| 47 | bad | good | good | لا | لا | لا |
| 48 | good | good | good | لا | لا | نعم |
| 49 | good | good | good | لا | لا | نعم |
| 50 | good | bad | bad | لا | لا | نعم |
| 51 | bad | bad | bad | لا | لا | لا |
| 52 | bad | good | bad | لا | لا | لا |
| 53 | bad | bad | good | لا | لا | لا |
| 54 | good | good | good | لا | لا | لا |
| 55 | good | good | good | لا | لا | لا |
| 56 | bad | good | good | لا | لا | نعم |
| 57 | bad | good | good | لا | لا | لا |
| 58 | good | good | good | لا | لا | لا |
| 59 | good | good | good | لا | لا | لا |
| 60 | good | good | good | لا | لا | نعم |
| 61 | good | good | good | لا | لا | نعم |
| 62 | good | good | good | لا | لا | نعم |
| 63 | bad | bad | good | لا | لا | لا |
| 64 | bad | good | good | لا | لا | لا |
| 65 | good | good | good | لا | لا | لا |
| 66 | good | good | good | لا | لا | نعم |
| 67 | bad | good | good | لا | لا | لا |
| 68 | good | good | good | نعم | لا | نعم |
| 69 | good | good | good | لا | لا | نعم |
| 70 | good | good | good | لا | لا | لا |
| 71 | good | good | good | لا | لا | لا |
| 72 | good | good | good | لا | لا | نعم |
| 73 | good | good | bad | لا | لا | لا |
| 74 | bad | bad | good | لا | لا | لا |
| 75 | good | good | good | لا | لا | نعم |
| 76 | bad | good | good | لا | لا | نعم |
| 77 | good | good | good | لا | لا | نعم |
| 78 | good | good | good | لا | لا | نعم |
| 79 | good | bad | bad | نعم | لا | لا |
| 80 | bad | good | good | لا | لا | لا |
| 81 | good | good | bad | لا | لا | نعم |
| 82 | bad | good | good | لا | لا | لا |
| 83 | bad | good | good | لا | لا | لا |
| 84 | bad | good | good | لا | لا | لا |
| 85 | bad | bad | good | نعم | لا | لا |
| 86 | bad | good | good | نعم | لا | لا |
| 87 | good | good | good | لا | لا | نعم |
| 88 | good | good | good | لا | لا | نعم |
| 89 | bad | good | good | لا | لا | لا |
| 90 | bad | good | good | نعم | لا | لا |
| 91 | good | good | good | لا | لا | نعم |
| 92 | bad | good | good | لا | لا | نعم |
| 93 | good | bad | good | لا | لا | نعم |
| 94 | good | good | good | لا | لا | لا |
| 95 | bad | good | good | لا | لا | لا |
| 96 | good | good | good | لا | لا | لا |
| 97 | bad | good | good | لا | لا | لا |
| 98 | bad | good | good | لا | لا | لا |
| 99 | good | good | good | لا | لا | نعم |
| 100 | bad | bad | good | نعم | لا | لا |
| 101 | good | good | good | لا | لا | نعم |
| 102 | good | good | good | لا | لا | نعم |
| 103 | bad | bad | good | لا | لا | لا |
| 104 | good | good | good | لا | لا | نعم |
| 105 | good | good | bad | لا | لا | نعم |
| 106 | good | good | bad | لا | لا | لا |
| 107 | bad | good | good | لا | لا | نعم |
| 108 | good | good | good | لا | لا | نعم |
| 109 | bad | good | bad | لا | لا | لا |
| 110 | bad | good | good | لا | لا | نعم |
| 111 | good | good | good | لا | لا | نعم |
| 112 | good | good | good | لا | لا | لا |
| 113 | good | good | good | لا | لا | لا |
| 114 | bad | bad | good | لا | لا | لا |
| 115 | bad | good | good | لا | لا | لا |
| 116 | bad | bad | good | لا | لا | لا |
| 117 | bad | good | good | لا | لا | لا |
| 118 | good | good | good | لا | لا | لا |
| 119 | good | good | good | لا | لا | نعم |
| 120 | good | bad | bad | نعم | لا | لا |
| 121 | good | good | good | لا | لا | لا |
| 122 | bad | good | good | لا | لا | لا |
| 123 | good | good | good | لا | لا | نعم |
| 124 | good | good | bad | لا | لا | نعم |
| 125 | good | good | bad | لا | لا | نعم |
| 126 | good | good | good | لا | لا | نعم |
| 127 | bad | good | bad | لا | لا | نعم |
| 128 | bad | good | good | لا | لا | لا |
| 129 | good | bad | good | لا | لا | نعم |
| 130 | good | bad | good | لا | لا | نعم |
| 131 | bad | good | good | لا | لا | لا |
| 132 | good | good | good | لا | لا | لا |
| 133 | bad | good | good | لا | لا | لا |
| 134 | bad | bad | good | لا | لا | نعم |
| 135 | bad | good | good | لا | لا | نعم |
| 136 | bad | good | good | لا | لا | لا |
| 137 | bad | good | bad | لا | لا | لا |
| 138 | bad | good | good | لا | لا | لا |
| 139 | good | bad | good | لا | لا | نعم |
| 140 | good | good | good | لا | لا | نعم |
| 141 | good | good | good | لا | لا | نعم |
| 142 | bad | good | good | لا | لا | لا |
| 143 | good | good | good | لا | لا | نعم |
| 144 | bad | good | good | لا | لا | نعم |
| 145 | good | bad | good | لا | لا | نعم |
| 146 | good | good | bad | لا | لا | نعم |
| 147 | bad | good | good | لا | لا | لا |
| 148 | good | bad | good | نعم | لا | نعم |
| 149 | good | good | bad | لا | لا | نعم |
| 150 | bad | good | good | لا | لا | لا |
| 151 | bad | good | good | نعم | لا | لا |
| 152 | good | good | good | نعم | لا | نعم |
| 153 | good | good | good | لا | لا | نعم |
| 154 | good | good | bad | لا | لا | نعم |
| 155 | good | good | good | لا | لا | نعم |
| 156 | good | good | bad | لا | لا | لا |
| 157 | good | good | bad | لا | لا | نعم |
| 158 | bad | good | good | لا | لا | لا |
| 159 | good | good | good | لا | لا | نعم |
| 160 | good | good | good | لا | لا | نعم |
| 161 | good | good | good | لا | لا | لا |
| 162 | good | bad | bad | لا | لا | نعم |
| 163 | bad | bad | bad | لا | لا | لا |
| 164 | bad | good | good | لا | لا | لا |
| 165 | good | good | bad | لا | لا | نعم |
| 166 | bad | good | good | لا | لا | لا |
| 167 | bad | good | bad | لا | لا | لا |
| 168 | bad | good | good | لا | لا | لا |
| 169 | good | good | bad | لا | لا | نعم |
| 170 | good | good | good | لا | لا | نعم |
| 171 | bad | good | good | لا | لا | لا |
| 172 | good | good | bad | لا | لا | نعم |
| 173 | good | good | good | لا | لا | نعم |
| 174 | bad | good | good | لا | لا | لا |
| 175 | bad | good | good | لا | لا | لا |
| 176 | good | bad | good | لا | لا | لا |
| 177 | good | good | good | نعم | لا | لا |
| 178 | good | good | good | لا | لا | نعم |
| 179 | bad | good | good | لا | لا | لا |
| 180 | good | good | good | لا | نعم | نعم |
| 181 | good | good | bad | لا | لا | نعم |
| 182 | good | good | good | لا | لا | نعم |
| 183 | good | good | good | لا | لا | نعم |
| 184 | good | good | good | لا | لا | نعم |
| 185 | good | good | good | لا | لا | نعم |
| 186 | good | good | good | لا | لا | لا |
| 187 | bad | good | bad | نعم | لا | لا |
| 188 | good | bad | bad | لا | لا | نعم |
| 189 | bad | good | good | لا | لا | لا |
| 190 | good | good | good | لا | لا | نعم |
| 191 | bad | good | good | لا | لا | لا |
| 192 | good | good | good | لا | لا | نعم |
| 193 | good | good | good | لا | لا | لا |
| 194 | good | good | good | لا | لا | نعم |
| 195 | good | good | bad | لا | لا | نعم |
| 196 | bad | good | bad | لا | لا | لا |
| 197 | good | good | good | لا | لا | نعم |
| 198 | bad | good | good | لا | لا | لا |
| 199 | good | bad | good | لا | لا | نعم |
| 200 | good | good | good | لا | لا | نعم |
| 201 | good | good | bad | لا | لا | نعم |
| 202 | good | good | good | لا | لا | نعم |
| 203 | good | good | good | لا | لا | نعم |
| 204 | bad | bad | good | لا | لا | لا |
| 205 | bad | good | bad | لا | لا | لا |
| 206 | good | good | good | لا | لا | نعم |
| 207 | good | good | good | لا | لا | نعم |
| 208 | good | good | good | لا | لا | نعم |
| 209 | bad | good | good | لا | لا | لا |
| 210 | good | good | good | لا | لا | لا |
| 211 | bad | good | good | لا | لا | لا |
| 212 | bad | good | good | لا | لا | لا |
| 213 | bad | good | good | لا | لا | لا |
| 214 | bad | good | good | لا | لا | لا |
| 215 | bad | good | good | لا | لا | لا |
| 216 | bad | good | good | لا | لا | نعم |
| 217 | bad | bad | good | لا | لا | لا |
| 218 | good | good | good | لا | لا | لا |
| 219 | bad | good | good | لا | لا | لا |
| 220 | good | good | good | لا | لا | نعم |
| 221 | bad | good | good | لا | لا | نعم |
| 222 | bad | good | good | لا | لا | لا |
| 223 | bad | bad | good | لا | لا | لا |
| 224 | good | good | good | لا | لا | لا |
| 225 | bad | good | good | لا | لا | لا |
| 226 | good | good | good | لا | لا | لا |
| 227 | bad | good | good | لا | لا | نعم |
| 228 | good | good | good | لا | لا | نعم |
| 229 | good | good | good | لا | لا | لا |
| 230 | bad | bad | good | نعم | لا | لا |
| 231 | good | bad | good | نعم | لا | نعم |
| 232 | good | good | good | لا | لا | نعم |
| 233 | good | good | good | لا | لا | لا |
| 234 | good | good | good | لا | لا | نعم |
| 235 | good | good | good | لا | لا | نعم |
| 236 | bad | good | good | لا | لا | لا |
| 237 | good | bad | good | لا | لا | لا |
| 238 | good | good | good | لا | لا | نعم |
| 239 | good | bad | bad | لا | لا | لا |
| 240 | bad | good | bad | لا | لا | لا |
| 241 | good | good | good | لا | لا | نعم |
| 242 | good | good | good | لا | لا | لا |
| 243 | good | good | good | لا | لا | نعم |
| 244 | good | good | good | لا | لا | نعم |
| 245 | good | good | good | لا | لا | لا |
| 246 | good | good | good | لا | لا | لا |
| 247 | bad | good | bad | لا | لا | لا |
| 248 | bad | good | good | لا | لا | لا |
| 249 | good | good | good | لا | لا | نعم |
| 250 | good | good | good | لا | لا | لا |
| 251 | bad | good | bad | لا | نعم | لا |
| 252 | bad | good | good | لا | لا | نعم |
| 253 | good | good | good | لا | لا | لا |
| 254 | good | good | good | لا | لا | نعم |
| 255 | good | good | good | لا | لا | نعم |
| 256 | good | good | good | لا | لا | نعم |
| 257 | good | good | good | لا | لا | نعم |
| 258 | bad | bad | good | لا | لا | نعم |
| 259 | bad | good | good | لا | لا | نعم |
| 260 | good | good | bad | لا | لا | نعم |
| 261 | good | good | bad | لا | لا | نعم |
| 262 | bad | good | good | لا | لا | لا |
| 263 | good | good | good | لا | لا | نعم |
| 264 | good | good | good | لا | لا | نعم |
| 265 | bad | good | good | لا | لا | لا |
| 266 | bad | good | good | لا | لا | لا |
| 267 | good | good | good | لا | لا | لا |
| 268 | good | good | good | لا | لا | نعم |
| 269 | good | bad | bad | نعم | لا | لا |
| 270 | good | bad | good | لا | لا | نعم |
| 271 | good | good | good | نعم | لا | نعم |
| 272 | good | good | good | لا | لا | نعم |
| 273 | bad | good | bad | لا | لا | لا |
| 274 | bad | good | good | لا | لا | نعم |
| 275 | good | good | good | لا | لا | نعم |
| 276 | bad | good | good | لا | لا | لا |
| 277 | good | good | good | لا | لا | نعم |
| 278 | good | bad | good | نعم | لا | لا |
| 279 | bad | good | good | لا | لا | لا |
| 280 | good | good | good | لا | لا | نعم |
| 281 | bad | good | good | لا | لا | لا |
| 282 | bad | good | good | لا | لا | لا |
| 283 | bad | good | good | لا | لا | لا |
| 284 | good | good | good | لا | لا | نعم |
| 285 | bad | bad | good | نعم | لا | لا |
| 286 | good | good | good | نعم | لا | لا |
| 287 | good | good | good | لا | لا | نعم |
| 288 | good | bad | good | لا | لا | لا |
| 289 | good | good | good | لا | لا | نعم |
| 290 | bad | good | good | لا | لا | لا |
| 291 | bad | bad | good | لا | لا | لا |
| 292 | bad | bad | good | لا | لا | نعم |
| 293 | good | good | good | لا | لا | نعم |
| 294 | bad | good | good | نعم | لا | لا |
| 295 | good | good | bad | لا | لا | لا |
| 296 | bad | good | good | لا | لا | لا |
| 297 | bad | bad | good | لا | لا | نعم |
| 298 | bad | good | good | لا | لا | لا |
| 299 | good | good | bad | لا | لا | نعم |
| 300 | good | bad | bad | لا | لا | نعم |
| 301 | good | good | good | لا | لا | نعم |
| 302 | good | good | good | لا | لا | لا |
| 303 | bad | good | good | لا | لا | نعم |
| 304 | good | good | good | لا | لا | نعم |
| 305 | good | good | good | لا | لا | نعم |
| 306 | bad | good | good | لا | لا | لا |
| 307 | bad | good | good | لا | لا | لا |
| 308 | bad | bad | good | لا | لا | نعم |
| 309 | bad | good | good | لا | لا | لا |
| 310 | bad | good | bad | لا | لا | لا |
| 311 | bad | good | bad | لا | لا | نعم |
| 312 | bad | bad | bad | لا | لا | لا |
| 313 | good | good | good | لا | لا | لا |
| 314 | bad | bad | good | لا | لا | لا |
| 315 | good | good | good | لا | لا | نعم |
| 316 | good | bad | bad | لا | لا | نعم |
| 317 | good | good | bad | لا | لا | لا |
| 318 | bad | good | good | لا | لا | لا |
| 319 | good | bad | bad | نعم | لا | نعم |
| 320 | bad | good | good | لا | لا | نعم |
| 321 | bad | good | bad | لا | لا | لا |
| 322 | good | good | good | لا | لا | نعم |
| 323 | good | bad | bad | لا | لا | نعم |
| 324 | good | good | good | لا | لا | لا |
| 325 | good | good | bad | لا | لا | لا |
| 326 | bad | good | good | لا | لا | نعم |
| 327 | good | good | good | لا | لا | نعم |
| 328 | bad | good | bad | لا | لا | لا |
| 329 | good | good | good | لا | لا | نعم |
| 330 | bad | good | good | لا | لا | لا |
| 331 | good | good | bad | لا | لا | نعم |
| 332 | bad | bad | good | لا | لا | لا |
| 333 | bad | good | good | لا | لا | نعم |
| 334 | good | good | good | لا | لا | نعم |
| 335 | good | good | bad | لا | لا | نعم |
| 336 | good | good | good | لا | لا | نعم |
| 337 | bad | good | good | لا | لا | لا |
| 338 | bad | bad | good | لا | لا | لا |
| 339 | bad | good | good | لا | لا | لا |
| 340 | good | bad | bad | نعم | لا | لا |
| 341 | bad | bad | good | لا | لا | نعم |
| 342 | good | good | good | لا | لا | نعم |
| 343 | bad | good | good | لا | لا | لا |
| 344 | good | good | good | لا | لا | لا |
| 345 | bad | good | good | لا | لا | لا |
| 346 | bad | good | good | لا | لا | نعم |
| 347 | bad | good | good | لا | لا | لا |
| 348 | good | good | good | لا | لا | نعم |
| 349 | good | bad | good | لا | لا | نعم |
| 350 | bad | bad | bad | لا | لا | لا |
| 351 | good | good | good | لا | لا | لا |
| 352 | good | bad | good | نعم | لا | لا |
| 353 | bad | bad | bad | لا | لا | لا |
| 354 | good | good | good | لا | لا | نعم |
| 355 | good | good | good | لا | لا | نعم |
| 356 | good | good | good | لا | لا | نعم |
| 357 | bad | good | good | لا | لا | لا |
| 358 | good | good | good | لا | لا | نعم |
| 359 | bad | good | good | لا | لا | لا |
| 360 | bad | good | good | لا | لا | نعم |
| 361 | bad | bad | good | لا | لا | لا |
| 362 | bad | good | good | لا | لا | لا |
| 363 | good | bad | good | لا | لا | لا |
| 364 | bad | good | good | لا | لا | نعم |
| 365 | bad | good | good | لا | لا | لا |
| 366 | good | good | good | لا | لا | نعم |
| 367 | bad | good | good | لا | لا | نعم |
| 368 | good | bad | good | لا | لا | نعم |
| 369 | good | good | bad | لا | لا | لا |
| 370 | bad | good | good | لا | لا | لا |
| 371 | bad | good | good | لا | لا | لا |
| 372 | bad | good | good | لا | لا | لا |
| 373 | good | good | good | لا | لا | نعم |
| 374 | bad | good | good | لا | لا | لا |
| 375 | bad | good | good | لا | لا | نعم |
| 376 | good | good | good | لا | لا | لا |
| 377 | good | good | good | لا | لا | نعم |
| 378 | bad | bad | good | لا | لا | لا |
| 379 | good | bad | bad | لا | لا | نعم |
| 380 | good | good | good | لا | لا | نعم |
| 381 | bad | bad | good | لا | لا | نعم |
| 382 | bad | good | good | لا | لا | لا |
| 383 | bad | good | good | لا | لا | لا |
| 384 | bad | good | good | لا | لا | لا |
| 385 | good | bad | good | نعم | لا | لا |
| 386 | good | good | good | لا | لا | لا |
| 387 | good | good | good | لا | لا | نعم |
| 388 | bad | good | bad | لا | لا | نعم |
| 389 | good | good | good | لا | لا | نعم |
| 390 | bad | good | good | لا | لا | نعم |
| 391 | bad | good | good | لا | لا | لا |
| 392 | bad | bad | good | لا | لا | لا |
| 393 | bad | good | good | لا | لا | لا |
| 394 | good | good | bad | لا | لا | لا |
| 395 | bad | good | good | لا | لا | لا |
| 396 | bad | good | bad | لا | لا | نعم |
| 397 | bad | bad | good | لا | لا | لا |
| 398 | good | good | good | لا | لا | لا |
| 399 | bad | good | good | لا | لا | لا |
| 400 | good | good | good | لا | لا | لا |
| 401 | bad | good | good | لا | لا | لا |
| 402 | good | good | good | لا | لا | نعم |
| 403 | good | good | good | لا | لا | لا |
| 404 | good | good | good | لا | لا | نعم |
| 405 | good | good | good | لا | لا | نعم |
| 406 | bad | good | good | لا | لا | لا |
| 407 | good | good | good | لا | لا | نعم |
| 408 | good | good | good | نعم | لا | لا |
| 409 | bad | good | bad | لا | لا | لا |
| 410 | bad | good | good | لا | لا | لا |
| 411 | good | good | good | لا | لا | نعم |
| 412 | bad | good | good | لا | لا | لا |
| 413 | good | good | good | لا | لا | نعم |
| 414 | good | bad | bad | لا | لا | نعم |
| 415 | bad | good | good | لا | لا | لا |
| 416 | good | good | good | لا | لا | نعم |
| 417 | good | good | bad | لا | نعم | لا |
| 418 | bad | good | good | لا | لا | لا |
| 419 | good | good | good | لا | لا | لا |
| 420 | good | good | good | لا | لا | نعم |
| 421 | bad | good | good | لا | لا | لا |
| 422 | good | good | good | لا | لا | لا |
| 423 | good | bad | good | لا | لا | نعم |
| 424 | good | good | good | لا | لا | لا |
| 425 | good | good | good | لا | لا | نعم |
| 426 | bad | good | good | لا | لا | لا |
| 427 | bad | good | bad | لا | لا | نعم |
| 428 | good | good | good | لا | لا | لا |
| 429 | good | good | bad | لا | لا | نعم |
| 430 | good | good | good | لا | لا | نعم |
| 431 | bad | good | good | لا | لا | لا |
| 432 | bad | good | good | لا | لا | لا |
| 433 | good | bad | bad | نعم | لا | لا |
| 434 | good | bad | good | لا | لا | لا |
| 435 | good | good | good | لا | لا | نعم |
| 436 | bad | bad | good | لا | لا | لا |
| 437 | good | good | bad | لا | لا | لا |
| 438 | bad | good | good | لا | لا | لا |
| 439 | good | good | good | لا | لا | نعم |
| 440 | bad | good | bad | لا | لا | لا |
| 441 | bad | good | good | لا | لا | لا |
| 442 | bad | good | good | لا | لا | لا |
| 443 | good | good | good | لا | لا | نعم |
| 444 | bad | good | good | لا | لا | لا |
| 445 | good | good | good | لا | لا | لا |
| 446 | good | bad | good | لا | لا | نعم |
| 447 | good | good | good | لا | لا | نعم |
| 448 | bad | good | good | لا | لا | لا |
| 449 | good | good | good | نعم | لا | نعم |
| 450 | good | good | good | لا | لا | لا |
| 451 | bad | good | good | لا | لا | نعم |
| 452 | good | good | good | لا | لا | نعم |
| 453 | bad | good | good | لا | لا | لا |
| 454 | good | good | bad | لا | لا | نعم |
| 455 | good | good | bad | لا | لا | نعم |
| 456 | good | good | bad | لا | لا | لا |
| 457 | bad | good | good | لا | لا | نعم |
| 458 | good | good | good | لا | لا | نعم |
| 459 | good | good | good | نعم | لا | نعم |
| 460 | good | good | good | لا | لا | نعم |
| 461 | good | good | good | لا | لا | نعم |
| 462 | bad | good | good | لا | لا | لا |
| 463 | bad | bad | good | لا | لا | لا |
| 464 | good | bad | good | لا | لا | لا |
| 465 | bad | good | bad | لا | لا | نعم |
| 466 | bad | bad | good | لا | لا | لا |
| 467 | good | good | good | لا | لا | لا |
| 468 | bad | good | good | لا | لا | لا |
| 469 | good | good | good | لا | لا | نعم |
| 470 | good | good | good | لا | لا | نعم |
| 471 | good | bad | good | لا | لا | نعم |
| 472 | bad | good | good | لا | لا | لا |
| 473 | good | good | good | لا | لا | نعم |
| 474 | good | good | bad | لا | لا | نعم |
| 475 | bad | good | good | لا | لا | لا |
| 476 | good | good | good | لا | لا | نعم |
| 477 | bad | bad | good | لا | لا | نعم |
| 478 | good | good | good | لا | لا | لا |
| 479 | good | good | good | لا | لا | نعم |
| 480 | good | bad | good | لا | لا | نعم |
| 481 | bad | bad | bad | لا | لا | لا |
| 482 | good | good | good | لا | لا | نعم |
| 483 | good | good | good | لا | لا | نعم |
| 484 | bad | good | good | لا | لا | لا |
| 485 | good | good | good | لا | لا | نعم |
| 486 | good | good | good | لا | لا | لا |
| 487 | bad | bad | good | لا | لا | لا |

## ما الذي يبقى غير محسوم؟
- مطابقة الإجابة للمصدر الأصلي في كل حالة، لأن الملف لا يضم النص الكامل لجميع الوثائق.
- وجود أمثلة Python في المصدر المسترجع عند غياب أمثلة من الإجابة.
- هل أوضح Agent أسباب عمليات البحث/الاسترجاع في رسائل وسيطة غير محفوظة؟ سجل الأدوات هنا يحفظ أسماء الاستدعاءات ووسائطها ولا يحفظ تلك الرسائل.
- إثبات أن كل استرجاع زائد غير ضروري: لا تكفي أسماء الملفات وحدها.

## قرار التنفيذ
نوصي بتصحيح Prompt التقييم لا بتغيير نتائج التشغيل الأصلية، وبحفظ الأحكام الآلية إلى جانب الملاحظات المثبتة، ثم مراجعة عينة بشرية متنوعة مع الاطلاع على صفحات المصدر. تجنب وصف نسب الـ Judges بأنها دقة بشرية.