#!/bin/bash -x

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

START_FILE="${1}"
if [ -z "${START_FILE}" ]; then
    echo "Please provide a start sqlite database."
    exit 1
fi

txtOutDir="/tmp/wikiGenPages"
yamlOutDir="/tmp/yamlOutDir"
mkdir -p ${txtOutDir}
#rm -rf ${yamlOutDir}
mkdir -p ${yamlOutDir}
python3 ${SCRIPT_DIR}/pullPagesFromDatabase.py ${START_FILE} ${txtOutDir}
for FILE in ${txtOutDir}/*; do
    f="$(basename -- $FILE)"
    ${SCRIPT_DIR}/mwtoast -i ${FILE} > ${yamlOutDir}/${f}.yaml
done

htmlOutDir="/tmp/htmlOutDir"
rm -rf ${htmlOutDir}
mkdir -p ${htmlOutDir}
python3 ${SCRIPT_DIR}/wikiReconstructorTool.py -i ${yamlOutDir} -o ${htmlOutDir}
rm -rf ${txtOutDir}
