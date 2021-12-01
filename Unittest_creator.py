import os


years = [2021]
dir_base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
run_base = os.path.join(dir_base, ".idea/runConfigurations")
for year in years:
    for day_num in range(1, 25):
        day = "0" + str(day_num) if day_num < 10 else str(day_num)
        text = \
            '<component name="ProjectRunConfigurationManager">\
              <configuration default="false" name="Unittests in {year} Day{day}.py" type="tests" factoryName="Unittests" folderName="{year}" nameIsGenerated="false">\
                <module name="adventofcode" />\
                <option name="INTERPRETER_OPTIONS" value="" />\
                <option name="PARENT_ENVS" value="true" />\
                <option name="SDK_HOME" value="" />\
                <option name="WORKING_DIRECTORY" value="" />\
                <option name="IS_MODULE_SDK" value="false" />\
                <option name="ADD_CONTENT_ROOTS" value="true" />\
                <option name="ADD_SOURCE_ROOTS" value="true" />\
                <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />\
                <option name="_new_pattern" value="&quot;&quot;" />\
                <option name="_new_additionalArguments" value="&quot;&quot;" />\
                <option name="_new_target" value="&quot;$PROJECT_DIR$/{year}/Day{day}.py&quot;" />\
                <option name="_new_targetType" value="&quot;PATH&quot;" />\
                <method v="2" />\
              </configuration>\
            </component>'.format(day=day, year=year)
        filepath = os.path.join(run_base, "Unittests_in_" + str(year) + "_Day" + day + "_py.xml")
        if os.path.exists(filepath):
            with open(filepath, "w") as file:
                file.write(text)
        else:
            with open(filepath, "x") as file:
                file.write(text)
