#pragma once

#include <cassert>
#include <cstring>

#include "common/types/ku_list.h"

namespace kuzu {
namespace function {
namespace operation {

struct ListPrepend {
    template<typename T>
    static inline void operation(T& value, common::list_entry_t& listEntry,
        common::list_entry_t& result, common::ValueVector& valueVector,
        common::ValueVector& listVector, common::ValueVector& resultVector) {
        result = common::ListVector::addList(&resultVector, listEntry.size + 1);
        auto listValues = common::ListVector::getListValues(&listVector, listEntry);
        auto listDataVector = common::ListVector::getDataVector(&listVector);
        auto resultValues = common::ListVector::getListValues(&resultVector, result);
        auto resultDataVector = common::ListVector::getDataVector(&resultVector);
        auto numBytesPerValue = resultDataVector->getNumBytesPerValue();
        common::ValueVectorUtils::copyValue(
            resultValues, *resultDataVector, reinterpret_cast<uint8_t*>(&value), valueVector);
        resultValues += numBytesPerValue;
        for (auto i = 0u; i < listEntry.size; i++) {
            common::ValueVectorUtils::copyValue(
                resultValues, *resultDataVector, listValues, *listDataVector);
            listValues += numBytesPerValue;
            resultValues += numBytesPerValue;
        }
    }
};

} // namespace operation
} // namespace function
} // namespace kuzu
