STACK_NAME = s3strm-backend
STACK_TEMPLATE = file://./cfn.yml
ACTION := $(shell ./bin/cloudformation_action $(STACK_NAME))

URLGENERATOR_KEY = $(shell make -C lambdas/urlgenerator/src lambda_key)

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
	  --capabilities CAPABILITY_IAM                                         \
	  2>&1
	@aws cloudformation wait stack-${ACTION}-complete \
	  --stack-name ${STACK_NAME}

upload:
	@make -C lambdas/urlgenerator/src upload

integration_test:
	./test/test_urlgenerator

