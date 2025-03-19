generate:
	java -jar modules/swagger-codegen-cli/target/swagger-codegen-cli.jar generate \
 	-i modules/swagger-codegen/src/test/resources/2_0/petstore.json -l perl \
 	--git-user-id "swaggerapi" \
 	--git-repo-id "petstore-perl" \
 	--release-note "Github integration demo" \
 	-o /var/tmp/perl/petstore