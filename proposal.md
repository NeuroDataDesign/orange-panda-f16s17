1. Problem Statement
    1. What is the broadly important real-world problem (or class of problems) we are going to solve?
        - Many psychological disorders share symptoms and biomarkers. Many previous research studies have attempted to associate individual behavioral disorders with individual brain activity, but due to the similarities of disorders and potential biomarkers, research needs to look at multiple biomarkers and see how they affect multiple disorders so that we get a multi-dimensional view of disorders, and can thus differentiate between them with a broader and deeper understanding.
    2. What will be required to solve that problem?
        1. Data
            - We currently have 126 data samples from EEG data sharing paper from Jovo. Because this data corresponds to potentially an assortment of mental illnesses (that we don't know for sure), we need other data for similar biomarkers in order to make confident correlations. We also want to look into finding some control data under similar circumstances so that we can compare. Also, we may want to see if other situations/biomarkers may provide a bigger sample size (this can open doors for other brian activity areas, wearables, etc.).
        2. Technology
            - We won't need EEG headsets (we want already made data), but we want EEG headsets to become more of a standard in psychiatric treatment. We will need to use EEG analysis to find correlations in the data. In addition, we need to have some sort of machine learning model that can:
                - Learn from the available data
                - Handle many, many layers of inputs and potential biomarkers
                - Has room to grow when we find additional relevant biomarkers/someone else finds relevant biomarkers
        3. Funding
            - Right now $0 as all data we have is being found/given (unless we're mistaken). Potentially increase the funding to host the algorithm via a web app. Also, instead of direct funding, we could use the Hopkins coursera courses for Biostatistics for free.
        4. Societal stuff?
            - Psychiatric treatment needs to standardize related biomarker tests and use them actively. This will both increase the potential data available to us and will improve treatment ability. As this shift happens, however, this research will not be as relevant. Also, the research world must start to move towards more multimodal and dimensional experiments on mental disorders.
    3. What scientific questions will we answered?
            - Are there correlations between disorders and the responses to the stimuli in the data?
            - Can you distinguish between multiple mental disorders by finding similar responses to multiple stimuli?
    4. What deliverable will we provide to the global citizens?
            - Web app that can receive uploaded EEG data regarding different tasks and provide classifications/probabilities with different potential mental disorders
2. Feasibility
    1. Background
        1. What is the current state of knowledge regarding this problem?
            - It's known that multiple biomarkers correspond with multiple mental diseases
            - We have multiple sets of correlations of brain activity (alongside other biomarkers) with different diseases
            - It's unknown when you look at multiple different biomarkers at once how they correlate with different diseases
        2. What are the key challenges?
            - Trying to assess already complicated data with multiple dimensions (i.e. 6 dimensions of EEG data, which likely means many many dimensions of relevant data)
        3. Has anyone made a concerted effort to solve the problem? Give examples. 
            - Our reference paper
        4. If so, what progress did they make, and why have they not succeeded?
            - They collected data, they didn't actually find connections within it
    2. Gap
        1. What gaps in scientific understanding must be bridged in order to solve this problem? 
            - How do different mental disorders react to different stimuli
        2. What gaps in technological  capabilities must be bridged in order to solve this problem? 
            - How do you analyze data with multiple dimensions via machine learning
        3. What organizational, financial, and/or technological challenges must be addressed in order to bridge these gaps?
            - More data, control subjects, etc.
    3. Work
        1. Why will this approach work? 
            - Because we have corresponding data with that aim that has not been used
        2. Why might it not, and what can be done to mitigate those challenges? 
            - Unfortunately, we have not been able to look at our data yet, and correlations may simply not exist between datas across those datasets
        3. How will you inspire financial support at the end of the year?
            - This is a relatively untouched area, so our entering it with novel data with a proven effective approach will see likely and important success.
3. Significance
    1. What tangible benefits would the world derive from solving this problem? For each of the below, provide specific/concrete numbers in absolute terms, and provide a meaningful point of reference (e.g., X costs 10 USD per year, which is Y fraction of medical spending)
        1. Economic
            - Save people money on misdiagnoses from general symptoms.
            - Also, will provide a more effective and quantitative basis for the diagnosis, saving money on psychiatrist trips.
        2. Medical
            - Will prevent misdiagnosis and will act as a building block for integrating other relevant and measurable factors that correlate with different diseases.
        3. Scientific
            - Will both increase our understanding on how different diseases affect different parts of our brain differently, but also our ability to understand the relationships between these diseases and their biomarkers.
        4. Societal
            - Will make handling and treatment of mental disorders on a large scale treatable.
    2. Which citizens of the world will be affected?
        - People with mental disorders and with potential for it.
4. Approach
    1. What is the approach for filling these gaps and solving the larger problem?
        - 
    2. What are each of the parts of the approach?
    3. How will each of these disparate parts be coordinated to bridge these gaps and then solve the larger problem? 
    4. How is this approach different from the status quo?
    5. How and when will success be measured/quantified?  Be as specific as possible.
    6. What does success look like at defined points along the roadmap?
    7. After 10 years, what does moderate success look like? What about huge success?