import os


years = [2019, 2020]
dir_base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
run_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".idea/runConfigurations")
for year in years:
    for day_num in range(1, 25):
        day = "0" + str(day_num) if day_num < 10 else str(day_num)
        text = \
            '<component name="ProjectRunConfigurationManager">\
              <configuration default="false" name="{year}-Day{day}" type="PythonConfigurationType" factoryName="Python" folderName="{year}">\
                <module name="adventofcode" />\
                <option name="INTERPRETER_OPTIONS" value="" />\
                <option name="PARENT_ENVS" value="true" />\
                <envs>\
                  <env name="PYTHONUNBUFFERED" value="1" />\
                </envs>\
                <option name="SDK_HOME" value="" />\
                <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$/{year}" />\
                <option name="IS_MODULE_SDK" value="false" />\
                <option name="ADD_CONTENT_ROOTS" value="true" />\
                <option name="ADD_SOURCE_ROOTS" value="true" />\
                <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />\
                <option name="SCRIPT_NAME" value="Day{day}" />\
                <option name="PARAMETERS" value="" />\
                <option name="SHOW_COMMAND_LINE" value="false" />\
                <option name="EMULATE_TERMINAL" value="false" />\
                <option name="MODULE_MODE" value="true" />\
                <option name="REDIRECT_INPUT" value="false" />\
                <option name="INPUT_FILE" value="" />\
                <method v="2">\
                  <option name="RunConfigurationTask" enabled="true" run_configuration_name="Unittests in {year} Day{day}.py" run_configuration_type="tests" />\
                </method>\
              </configuration>\
            </component>'.format(day=day, year=year)
        filepath = os.path.join(run_base, str(year) + "_Day" + day + ".xml")
        if os.path.exists(filepath):
            with open(filepath, "w") as file:
                file.write(text)
        else:
            with open(filepath, "x") as file:
                file.write(text)
