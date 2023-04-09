OUT_DIR=../../out

all: clean preprocess mix train

clean:
	@echo Cleaning
	@echo 	OUT_DIR = $(OUT_DIR)
	rm -rf $(OUT_DIR)

preprocess:
	@echo Preprocessing
	@python main.py preprocess

mix:
	@echo Mixing 
	@python main.py mix

train:
# 	@echo Training 
# 	@python main.py train
