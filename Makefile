STACK_NAME = s3strm-api
STACK_TEMPLATE = file://./cfn.yml
ACTION := $(shell ./bin/cloudformation_action $(STACK_NAME))

URLGENERATOR_KEY = $(shell make -C lambdas/urlgenerator/src lambda_key)
REFEEDER_KEY = $(shell make -C lambdas/refeeder/src lambda_key)
LISTER_KEY = $(shell make -C lambdas/lister/src lambda_key)

UPLOAD ?= true

export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION
export AWS_ACCESS_KEY_ID

.PHONY = deploy upload

deploy: upload
	aws cloudformation ${ACTION}-stack                                      \
	  --stack-name "${STACK_NAME}"                                          \
	  --template-body "${STACK_TEMPLATE}"                                   \
	  --parameters                                                          \
	    ParameterKey=URLGeneratorCodeKey,ParameterValue=${URLGENERATOR_KEY} \
	    ParameterKey=RefeederCodeKey,ParameterValue=${REFEEDER_KEY}         \
	    ParameterKey=ListerCodeKey,ParameterValue=${LISTER_KEY}             \
	  --capabilities CAPABILITY_IAM                                         \
	  2>&1
	@aws cloudformation wait stack-${ACTION}-complete \
	  --stack-name ${STACK_NAME}

upload:
ifeq ($(UPLOAD),true)
	@make -C lambdas/urlgenerator/src upload
	@make -C lambdas/refeeder/src upload
	@make -C lambdas/lister/src upload
endif

integration_test:
	./test/test_urlgenerator
