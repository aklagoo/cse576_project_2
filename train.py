from src.simplet5 import SimpleT5
import os
import pandas as pd
import h5py

if __name__=='__main__':
    path = os.getcwd()+"/data/pretrain/dataset.h5"
    f1 = h5py.File(path,'r+')
    train_df = []
    eval_df = []
    test_df = []


    #Inserting the train_data from the dataset.
    for data in f1['datasets']['format_1_mask_1d']['train']:
        train_df.append([data[1],data[0]])

    #Inserting the validation_data from the dataset.
    for data in f1['datasets']['format_1_mask_1d']['val']:
        eval_df.append([data[1],data[0]])

    #Inserting the test_data from the dataset.
    for data in f1['datasets']['format_1_mask_1d']['test']:
        test_df.append([data[1],data[0]])

    #Converting the numpy array to pandas Dataframe for train, test and val and converting the dataframe value to strings.
    train_df = pd.DataFrame(train_df, columns=['source_text','target_text'])
    train_df = train_df.applymap(str)
    eval_df = pd.DataFrame(eval_df, columns=['source_text','target_text'])
    eval_df = eval_df.applymap(str)
    test_df = pd.DataFrame(test_df, columns=['source_text','target_text'])
    test_df = test_df.applymap(str)

    model = SimpleT5()

    # load pretrained model.
    model.from_pretrained("t5","t5-base")


    # training the model by inputting the train and validation data.
    model.train(train_df=train_df, # pandas dataframe with 2 columns: source_text & target_text
                eval_df=eval_df, # pandas dataframe with 2 columns: source_text & target_text
                source_max_token_len = 512,
                target_max_token_len = 128,
                batch_size = 4,
                max_epochs = 5,
                use_gpu = True,
                outputdir = "outputs",
                early_stopping_patience_epochs = 0,
                precision = 32
                )

    # load trained T5 model
    model.load_model("t5","outputs/simplet5-epoch-4-train-loss", use_gpu=False)

    # predict
    ans = []
    total = 0
    correct = 0
    for index, row in test_df.iterrows():
        total +=1
        ans.append(model.predict(row['source_text']))
        if row['target_text'] == ans[index][0]:
            correct += 1
    print("accuracy" + " " + str(correct/total))