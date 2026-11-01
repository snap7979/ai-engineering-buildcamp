# الأسبوع السادس — مراجعة أدلة أول 20 حالة

**المنهج:** مراجعة مكتبية بمساعدة AI للملف الذي رفعه المستخدم، وليست مراجعة بشرية من 20 حالة. التقييم البشري الموثّق الوحيد هو الحالة 1.

**good/bad** = تقدير مدعوم بالنص أو قرار المستخدم للحالة الأولى؛ **uncertain** = لا يكفي الدليل للحسم. المراجعة لا تثبت صلاحية الكود أو صحة المرجع الأصلي دون الرجوع إلى الملفات المصدر.

| # | Judge (C/I/T) | مراجعة الأدلة (C/I/T) | سبب مختصر |
|---:|---|---|---|
| 1 | G/G/G | G/B/G | مخالفة مؤكدة: جواب النظام يتضمن pip install؛ حكم Instruction=good غير صحيح لهذا الشرط. تقييم المستخدم: Correctness=Good, Instruction=Bad, Trajectory=Good. |
| 2 | G/G/G | G/U/G | الجواب يتضمن Report وDataDriftPreset وتشغيله على مجموعتين؛ صحة الإجابة مدعومة بالمقارنة المرجعية. يلزم تدقيق تفاصيل API الإضافية. |
| 3 | G/G/B | G/U/U | الجواب يشمل id_column وtimestamp كما في المرجع. وصف الملف الثاني وحده لا يثبت عدم صلته؛ رفض Trajectory يحتاج فحصًا. |
| 4 | B/G/G | B/U/G | الإجابة تتحدث عن تصحيح الاختبارات عمومًا ولا تذكر فرز عمود Length كما في المرجع؛ إخفاق مطابقة واضح. |
| 5 | G/G/G | G/U/G | الإجابة تتضمن mean_error وerror std كما في المرجع؛ توافق مرجعي واضح. |
| 6 | B/B/G | B/U/G | المتطلب item_features غير مذكور؛ إخفاق مطابقة واضح. الحكم على وجوب مثال كود يحتاج معرفة محتوى الملفين. |
| 7 | G/B/G | B/U/G | الإجابة تخلط بين الأعمدة الفارغة والأعمدة غير المعرّفة ولا تصرح بإيقاف حساب drift ورفع خطأ؛ حكم Correctness=good قابل للاعتراض. |
| 8 | B/G/G | B/U/G | لم تذكر آلية DISAGREE أو شرط نسب النجاح 0 و1؛ إخفاق مطابقة واضح. |
| 9 | G/G/G | U/U/G | تغطية خيارات drift واسعة، لكن أمثلة API ينبغي التحقق منها مقابل الوثائق. |
| 10 | B/B/G | U/U/G | سؤال تصدير النتائج أجيب عنه مباشرة؛ المرجع يركز على العرض داخل Jupyter/Colab، ما يوحي بضعف ملاءمة السؤال المرجعي. رفض Correctness يحتاج مراجعة مصدر. |
| 11 | G/G/G | U/U/G | الجواب يؤكد إمكانية عدة تقييمات لكنه لا يوضح صراحة تقييم أعمدة متعددة وإرجاع درجات متعددة؛ قبول مشروط. |
| 12 | B/G/G | B/U/G | الجواب لا يذكر فئات relevant/irrelevant/partially relevant ولا placeholder؛ إخفاق مطابقة واضح. |
| 13 | G/G/G | G/U/G | الجواب يؤكد وجوب columns وذكر alias اختياري؛ متوافق. |
| 14 | G/G/G | G/U/G | الجواب يذكر قائمة Regression mappings؛ متوافق. |
| 15 | B/B/G | U/U/G | يوضح كيفية ضبط OPENAI_API_KEY عمليًا؛ Judge Correctness يرفض لغياب رابط Token page لا بسبب خطأ في الخطوات، وتقييم Instruction بأنه off-topic مشكوك فيه لأن وثائق Evidently تتضمن setup للمفتاح. |
| 16 | G/G/G | G/U/G | الجواب يشرح الإعدادات الافتراضية مع presets؛ متوافق. |
| 17 | G/G/G | G/U/G | الجواب يذكر 0.1 وشروط threshold؛ متوافق مع المرجع. |
| 18 | B/G/B | U/B/U | مخالفة مؤكدة: pip install موجود، وJudge أعطى Instruction=good. جواب Cloud يذكر الاتصال بالمشروع أيضًا؛ Correctness=bad يحتاج إعادة نظر. |
| 19 | G/G/G | G/U/G | الجواب يذكر binary classifier ومقارنة reference/current؛ متوافق. |
| 20 | B/B/G | B/U/G | الجواب لا يذكر BinaryClassificationPromptTemplate؛ إخفاق مطابقة واضح. الحكم على وجوب مثال كود يتطلب فحص المصدر. |

## دليل المراجعة التفصيلي

### الحالة 1

السؤال:

```text
Need to see the LLM jury example. Where's the code?
```

**الإجابة المرجعية:**

> Code example as a Jupyter notebook: https://github.com/evidentlyai/community-examples/blob/main/tutorials/LLM_as_a_jury_Example.ipynb

**ملخص ملاحظات المراجعة:** مخالفة مؤكدة: جواب النظام يتضمن pip install؛ حكم Instruction=good غير صحيح لهذا الشرط. تقييم المستخدم: Correctness=Good, Instruction=Bad, Trajectory=Good.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 2

السؤال:

```text
How do I create a report to check for data drift in my dataset?
```

**الإجابة المرجعية:**

> Let's generate a Data Drift preset that will check for statistical distribution changes between all columns in the dataset. ```python report = Report([ DataDriftPreset() ]) my_eval = report.run(eval_data_1, eval_data_2) ```

**ملخص ملاحظات المراجعة:** الجواب يتضمن Report وDataDriftPreset وتشغيله على مجموعتين؛ صحة الإجابة مدعومة بالمقارنة المرجعية. يلزم تدقيق تفاصيل API الإضافية.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 3

السؤال:

```text
How do I specify column roles when creating a DataDefinition?
```

**الإجابة المرجعية:**

> You can specify the ID column and timestamp in the `DataDefinition`, like this: `id_column='Id', timestamp='Date'`.

**ملخص ملاحظات المراجعة:** الجواب يشمل id_column وtimestamp كما في المرجع. وصف الملف الثاني وحده لا يثبت عدم صلته؛ رفض Trajectory يحتاج فحصًا.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=bad

### الحالة 4

السؤال:

```text
If the test fails, how do I figure out why?
```

**الإجابة المرجعية:**

> To find the failed output, you can sort the column "Length" in order and find the longest response.

**ملخص ملاحظات المراجعة:** الإجابة تتحدث عن تصحيح الاختبارات عمومًا ولا تذكر فرز عمود Length كما في المرجع؛ إخفاق مطابقة واضح.

**تقييم النموذج:** Correctness=bad, Instructions=good, Trajectory=good

### الحالة 5

السؤال:

```text
What kind of insights can I gain from `DummyMeanError()`?
```

**الإجابة المرجعية:**

> <ul><li>Calculates Mean Error for a dummy model.</li><li>Metric result: `mean_error`, `error std`.</li></ul>

**ملخص ملاحظات المراجعة:** الإجابة تتضمن mean_error وerror std كما في المرجع؛ توافق مرجعي واضح.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 6

السؤال:

```text
What does the diversity metric rely on?
```

**الإجابة المرجعية:**

> **Requirements**: You must pass the `item_features` list to point to numerical columns or embeddings that describe the recommended items. For example, these could be encoded genres that represent each movie.

**ملخص ملاحظات المراجعة:** المتطلب item_features غير مذكور؛ إخفاق مطابقة واضح. الحكم على وجوب مثال كود يحتاج معرفة محتوى الملفين.

**تقييم النموذج:** Correctness=bad, Instructions=bad, Trajectory=good

### الحالة 7

السؤال:

```text
What happens if my columns for testing are empty? Will it break anything?
```

**الإجابة المرجعية:**

> To evaluate data or prediction drift in the dataset, you need to ensure that the columns you test for drift are not empty. If these columns are empty in either reference or current data, Evidently will not calculate distribution drift and will raise an error.

**ملخص ملاحظات المراجعة:** الإجابة تخلط بين الأعمدة الفارغة والأعمدة غير المعرّفة ولا تصرح بإيقاف حساب drift ورفع خطأ؛ حكم Correctness=good قابل للاعتراض.

**تقييم النموذج:** Correctness=good, Instructions=bad, Trajectory=good

### الحالة 8

السؤال:

```text
What do I do if the judges disagree?
```

**الإجابة المرجعية:**

> To explicitly flag disagreements among LLMs, let’s add a custom descriptor. It will return "DISAGREE" if the success rate is not 0 or 1 (i.e., not unanimously rejected or approved).

**ملخص ملاحظات المراجعة:** لم تذكر آلية DISAGREE أو شرط نسب النجاح 0 و1؛ إخفاق مطابقة واضح.

**تقييم النموذج:** Correctness=bad, Instructions=good, Trajectory=good

### الحالة 9

السؤال:

```text
Can I customize how drift detection works? Like, what options do I have for that?
```

**الإجابة المرجعية:**

> You have multiple customization options.
> 
> * **Select columns**. You can apply Drift Detection only to some columns in the Dataset, for example, only to the important features. Use the `columns` parameter.
> 
> * **Change drift parameters.** You can modify how drift detection works:
> 
> * **Change methods**. Evidently has a large number of drift detection methods, including PSI, K-L divergence, Jensen-Shannon distance, Wasserstein distance, etc. You can also pick tests by column.
> 
> * **Change thresholds**. You can specify different drift detection conditions on the dataset or column level.
> 
> * **Implement a custom method**. You can implement a custom drift method as Python function.

**ملخص ملاحظات المراجعة:** تغطية خيارات drift واسعة، لكن أمثلة API ينبغي التحقق منها مقابل الوثائق.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 10

السؤال:

```text
Can I export these results somewhere after running my tests?
```

**الإجابة المرجعية:**

> This renders the Report directly in the interactive Python environment like Jupyter notebook or Colab. See other export options.

**ملخص ملاحظات المراجعة:** سؤال تصدير النتائج أجيب عنه مباشرة؛ المرجع يركز على العرض داخل Jupyter/Colab، ما يوحي بضعف ملاءمة السؤال المرجعي. رفض Correctness يحتاج مراجعة مصدر.

**تقييم النموذج:** Correctness=bad, Instructions=bad, Trajectory=good

### الحالة 11

السؤال:

```text
Can I run multiple evaluations at once with CustomDescriptor?
```

**الإجابة المرجعية:**

> You can also use `CustomDescriptor` to run evals for multiple columns and return multiple scores.

**ملخص ملاحظات المراجعة:** الجواب يؤكد إمكانية عدة تقييمات لكنه لا يوضح صراحة تقييم أعمدة متعددة وإرجاع درجات متعددة؛ قبول مشروط.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 12

السؤال:

```text
I want to classify text based on relevancy, how do I do that?
```

**الإجابة المرجعية:**

> To evaluate the relevance of an answer to the question, classify into 'relevant', 'irrelevant' and 'partially relevant'. Define the evaluation template with the question placeholder in your template.

**ملخص ملاحظات المراجعة:** الجواب لا يذكر فئات relevant/irrelevant/partially relevant ولا placeholder؛ إخفاق مطابقة واضح.

**تقييم النموذج:** Correctness=bad, Instructions=good, Trajectory=good

### الحالة 13

السؤال:

```text
Do the columns for semantic similarity need to be specified?
```

**الإجابة المرجعية:**

> **Required:** <ul><li>`columns`</li></ul>**Optional:** <ul><li> `alias`</li></ul>

**ملخص ملاحظات المراجعة:** الجواب يؤكد وجوب columns وذكر alias اختياري؛ متوافق.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 14

السؤال:

```text
Can I map multiple regression columns in one Dataset?
```

**الإجابة المرجعية:**

> You can have several regression results in the dataset, for example in case of multiple regression. (Pass the mappings in a list).

**ملخص ملاحظات المراجعة:** الجواب يذكر قائمة Regression mappings؛ متوافق.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 15

السؤال:

```text
I’m not sure how to set my OpenAI key as an environment variable... can someone help?
```

**الإجابة المرجعية:**

> Set up the OpenAI key ([Token page](https://platform.openai.com/api-keys)) as an environment variable. [See Open AI docs](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).

**ملخص ملاحظات المراجعة:** يوضح كيفية ضبط OPENAI_API_KEY عمليًا؛ Judge Correctness يرفض لغياب رابط Token page لا بسبب خطأ في الخطوات، وتقييم Instruction بأنه off-topic مشكوك فيه لأن وثائق Evidently تتضمن setup للمفتاح.

**تقييم النموذج:** Correctness=bad, Instructions=bad, Trajectory=good

### الحالة 16

السؤال:

```text
I’m trying to generate a report but I’m confused about how to run it. Can I just use defaults or do I need to change something?
```

**الإجابة المرجعية:**

> To generate a template Report, simply pass the selected Preset to the Report and run it over your data. If nothing else is specified, the Report will run with the default parameters for all columns in the dataset.

**ملخص ملاحظات المراجعة:** الجواب يشرح الإعدادات الافتراضية مع presets؛ متوافق.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 17

السؤال:

```text
Is there a specific threshold for drift detection in larger datasets?
```

**الإجابة المرجعية:**

> All metrics use a threshold = 0.1 by default. Drift score is distance/divergence. (>= 0.1 means drift).

**ملخص ملاحظات المراجعة:** الجواب يذكر 0.1 وشروط threshold؛ متوافق مع المرجع.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 18

السؤال:

```text
I'm trying to figure out how to start using the Evidently Cloud. What do I need to do first?
```

**الإجابة المرجعية:**

> You must first connect to [Evidently Cloud](/docs/setup/cloud) and [create a Project](/docs/platform/projects_manage).

**ملخص ملاحظات المراجعة:** مخالفة مؤكدة: pip install موجود، وJudge أعطى Instruction=good. جواب Cloud يذكر الاتصال بالمشروع أيضًا؛ Correctness=bad يحتاج إعادة نظر.

**تقييم النموذج:** Correctness=bad, Instructions=good, Trajectory=bad

### الحالة 19

السؤال:

```text
I'm trying to figure out how to detect embeddings drift for my model but I'm not sure what the default method is.
```

**الإجابة المرجعية:**

> The default embedding drift method is a **classifier**. Evidently trains a binary classification model to discriminate between data from reference and current distributions.

**ملخص ملاحظات المراجعة:** الجواب يذكر binary classifier ومقارنة reference/current؛ متوافق.

**تقييم النموذج:** Correctness=good, Instructions=good, Trajectory=good

### الحالة 20

السؤال:

```text
How do I check if my emails are appropriate? What do I use for judging?
```

**الإجابة المرجعية:**

> Use `BinaryClassificationPromptTemplate` to define what the LLM is judging.

**ملخص ملاحظات المراجعة:** الجواب لا يذكر BinaryClassificationPromptTemplate؛ إخفاق مطابقة واضح. الحكم على وجوب مثال كود يتطلب فحص المصدر.

**تقييم النموذج:** Correctness=bad, Instructions=bad, Trajectory=good
